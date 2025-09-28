import { Link } from "react-router"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
    Plane,
    Route,
    ArrowRight,
    Upload,
    FileSpreadsheet,
    CheckCircle,
    AlertCircle,
    Loader2,
    Folder
} from "lucide-react"
import { useState, useRef } from "react"
import * as XLSX from "xlsx"
import { toast } from "sonner"

interface ExcelFile {
    name: string
    data: any[]
    size: number
    file: File
}

interface ProcessResult {
    success: boolean
    message: string
    processed_count: number
    // Extended properties from upload-files API
    processed_files?: number
    total_rows?: number
    skipped_files?: number
    errors?: string[]
    file_details?: Array<{
        file_name: string
        file_type?: string
        rows: number
    }>
    processing_summary?: {
        raw_records: number
        processed_records: number
        error_records: number
        missing_actypes: number
        missing_routes: number
        imported_files: number
    }
}

const Index = () => {
    const [uploadedFiles, setUploadedFiles] = useState<ExcelFile[]>([])
    const [isUploading, setIsUploading] = useState(false)
    const [isProcessing, setIsProcessing] = useState(false)
    const [processResult, setProcessResult] = useState<ProcessResult | null>(null)

    // Reference input file to trigger programmatically
    const fileInputRef = useRef<HTMLInputElement>(null)
    const folderInputRef = useRef<HTMLInputElement>(null)

    // Helper function to check if a file is a valid Excel file
    const isExcelFile = (file: File): boolean => {
        return file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
            file.type === 'application/vnd.ms-excel' ||
            file.name.toLowerCase().endsWith('.xlsx') ||
            file.name.toLowerCase().endsWith('.xls')
    }

    // Function to recursively scan folder and extract Excel files
    const scanFolderForExcelFiles = async (items: DataTransferItemList): Promise<File[]> => {
        const files: File[] = []

        const traverseFileTree = async (item: any): Promise<void> => {
            return new Promise((resolve) => {
                if (item.isFile) {
                    item.file((file: File) => {
                        if (isExcelFile(file)) {
                            // Create a new file with the original name
                            const newFile = new File([file], file.name, { type: file.type })
                            files.push(newFile)
                        }
                        resolve()
                    })
                } else if (item.isDirectory) {
                    const dirReader = item.createReader()
                    dirReader.readEntries(async (entries: any[]) => {
                        const promises = entries.map(entry =>
                            traverseFileTree(entry)
                        )
                        await Promise.all(promises)
                        resolve()
                    })
                } else {
                    resolve()
                }
            })
        }

        const promises = []
        for (let i = 0; i < items.length; i++) {
            const item = items[i].webkitGetAsEntry()
            if (item) {
                promises.push(traverseFileTree(item))
            }
        }

        await Promise.all(promises)
        return files
    }

    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const files = Array.from(event.target.files || [])
        if (files.length === 0) return

        setIsUploading(true)

        // Filter only Excel files
        const excelFiles = files.filter(isExcelFile)

        if (excelFiles.length === 0) {
            toast.warning("Không có file Excel hợp lệ", {
                description: "Vui lòng chọn file có định dạng .xlsx hoặc .xls",
            })
            setIsUploading(false)
            return
        }

        // Show info about filtered files
        if (files.length > excelFiles.length) {
            const invalidCount = files.length - excelFiles.length
            toast.info("Đã lọc file", {
                description: `Tìm thấy ${excelFiles.length} file Excel hợp lệ, bỏ qua ${invalidCount} file khác.`,
            })
        }

        await processExcelFiles(excelFiles)
    }

    uploadedFiles.forEach((file) => {
        console.log(file.name)
    })

    const handleFolderUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const files = Array.from(event.target.files || [])
        files.forEach((file) => {
            console.log(file.name)
        })
        if (files.length === 0) return

        setIsUploading(true)

        // Filter only Excel files from the folder
        const excelFiles = files.filter(isExcelFile)

        if (excelFiles.length === 0) {
            toast.warning("Không có file Excel hợp lệ", {
                description: "Thư mục không chứa file Excel nào có định dạng .xlsx hoặc .xls",
            })
            setIsUploading(false)
            return
        }

        // Show info about found files
        if (files.length > excelFiles.length) {
            toast.info("Quét thư mục hoàn tất", {
                description: `Tìm thấy ${excelFiles.length} file Excel hợp lệ từ tổng ${files.length} file trong thư mục.`,
            })
        } else {
            toast.info("Quét thư mục hoàn tất", {
                description: `Tìm thấy ${excelFiles.length} file Excel trong thư mục.`,
            })
        }

        await processExcelFiles(excelFiles)
    }

    // Func to read each Excel file
    const processFile = (file: File): Promise<ExcelFile> => {
        return new Promise((resolve, reject) => {
            const reader = new FileReader()

            // Callback function after reading the file
            reader.onload = (e) => {
                try {
                    const data = new Uint8Array(e.target?.result as ArrayBuffer)
                    const workbook = XLSX.read(data, { type: 'array' })
                    const sheetName = workbook.SheetNames[0]
                    const worksheet = workbook.Sheets[sheetName]
                    const jsonData = XLSX.utils.sheet_to_json(worksheet)

                    resolve({
                        name: file.name,
                        data: jsonData,
                        size: jsonData.length,
                        file: file
                    })
                } catch (error) {
                    console.error('Lỗi khi đọc file Excel:', error)
                    reject(error)
                }
            }

            reader.readAsArrayBuffer(file)
        })
    }

    // Process Excel files function
    const processExcelFiles = async (files: File[]) => {
        // Process all files in parallel
        Promise.allSettled(files.map(processFile))
            .then(results => {
                const successfulFiles: ExcelFile[] = []
                const failedFiles: string[] = []

                // Classify results into successful and failed
                results.forEach((result, index) => {
                    if (result.status === 'fulfilled') {
                        successfulFiles.push(result.value)
                    } else {
                        failedFiles.push(files[index].name)
                    }
                })

                setUploadedFiles(prev => [...prev, ...successfulFiles])

                if (successfulFiles.length > 0) {
                    const totalRows = successfulFiles.reduce((sum, file) => sum + file.size, 0)
                    toast.success("Upload thành công", {
                        description: `Đã tải lên ${successfulFiles.length} file với tổng cộng ${totalRows} dòng dữ liệu`,
                    })
                }

                if (failedFiles.length > 0) {
                    toast.error("Lỗi khi đọc file", {
                        description: `Không thể đọc các file: ${failedFiles.join(', ')}`,
                    })
                }
            })
            .finally(() => {
                setIsUploading(false)
            })
    }

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault()
    }

    /**
     * Handle when user drop files/folders into upload area
     * - Support both files and folders
     * - Scan folders recursively for Excel files
     * - Process all found Excel files
     */
    const handleDrop = async (e: React.DragEvent) => {
        e.preventDefault()
        setIsUploading(true)

        try {
            // Check if dropped items include folders
            const items = e.dataTransfer.items
            let hasFolder = false

            for (let i = 0; i < items.length; i++) {
                const item = items[i].webkitGetAsEntry()
                if (item && item.isDirectory) {
                    hasFolder = true
                    break
                }
            }

            let allExcelFiles: File[] = []

            if (hasFolder) {
                // Handle folders - scan recursively for Excel files
                toast.info("Đang quét thư mục...", {
                    description: "Đang tìm kiếm file Excel trong thư mục đã kéo thả",
                })

                allExcelFiles = await scanFolderForExcelFiles(items)

                if (allExcelFiles.length === 0) {
                    toast.warning("Không tìm thấy file Excel", {
                        description: "Không có file Excel nào được tìm thấy trong thư mục đã kéo thả.",
                    })
                    setIsUploading(false)
                    return
                }

                toast.success("Quét thư mục hoàn tất", {
                    description: `Tìm thấy ${allExcelFiles.length} file Excel trong thư mục`,
                })
            } else {
                // Handle individual files
                const files = Array.from(e.dataTransfer.files)
                allExcelFiles = files.filter(isExcelFile)

                if (allExcelFiles.length === 0) {
                    toast.warning("File không hợp lệ", {
                        description: "Chỉ hỗ trợ file Excel (.xlsx, .xls).",
                    })
                    setIsUploading(false)
                    return
                }

                if (files.length > allExcelFiles.length) {
                    const invalidCount = files.length - allExcelFiles.length
                    toast.info("Đã lọc file", {
                        description: `Tìm thấy ${allExcelFiles.length} file Excel hợp lệ, bỏ qua ${invalidCount} file khác.`,
                    })
                }
            }

            // Process all found Excel files
            await processExcelFiles(allExcelFiles)
        } catch (error) {
            console.error('Error handling drop:', error)
            toast.error("Lỗi khi xử lý", {
                description: "Có lỗi xảy ra khi xử lý file/thư mục đã kéo thả.",
            })
            setIsUploading(false)
        }
    }

    /**
     * Process batch Excel data
     * - Use FormData to upload original files
     * - Call API batch upload endpoint
     * - Show toast notification for result
     * - Update processResult state
     */
    const processBatchExcelData = async (files: ExcelFile[]) => {
        setIsProcessing(true)

        try {
            // Prepare FormData with original files
            const formData = new FormData()
            files.forEach((fileData: ExcelFile) => {
                formData.append('files', fileData.file)
            })

            const response = await fetch(`${import.meta.env.VITE_API_URL}/data-processing/upload-files`, {
                method: 'POST',
                body: formData
            })

            if (!response.ok) {
                const errorText = await response.text()
                console.error('API Error Response:', errorText)

                toast.error("Lỗi khi xử lý dữ liệu", {
                    description: "Vui lòng thử lại.",
                })
                return
            }

            const result = await response.json()

            // Map all response fields to ProcessResult
            setProcessResult({
                success: result.success,
                message: result.message,
                processed_count: result.total_rows || 0,
                processed_files: result.processed_files,
                total_rows: result.total_rows,
                skipped_files: result.skipped_files,
                errors: result.errors,
                file_details: result.file_details,
                processing_summary: result.processing_summary,
            })

            if (result.success) {
                // Build detailed success message
                let description = result.message

                if (result.processed_files && result.total_rows) {
                    description += `\n📊 Đã xử lý: ${result.processed_files} file với ${result.total_rows} bản ghi`
                }

                if (result.skipped_files && result.skipped_files > 0) {
                    description += `\n⏭️ Đã bỏ qua: ${result.skipped_files} file đã import trước đó`
                }

                if (result.processing_summary) {
                    const summary = result.processing_summary
                    description += `\n✅ Processed: ${summary.processed_records} records`
                    if (summary.error_records > 0) {
                        description += `\n❌ Errors: ${summary.error_records} records`
                    }
                    if (summary.missing_actypes > 0 || summary.missing_routes > 0) {
                        description += `\n⚠️ Missing: ${summary.missing_actypes} actypes, ${summary.missing_routes} routes`
                    }
                }

                toast.success("Xử lý dữ liệu thành công", {
                    description: description,
                })
            } else {
                toast.error("Xử lý dữ liệu thất bại", {
                    description: result.message,
                })
            }

            // Handle errors array if present
            if (result.errors && result.errors.length > 0) {
                console.warn('Processing Errors:', result.errors)

                // Show first few errors as separate notifications
                result.errors.slice(0, 3).forEach((error: string, index: number) => {
                    setTimeout(() => {
                        toast.error(`Lỗi ${index + 1}`, {
                            description: error,
                        })
                    }, (index + 1) * 1000)
                })

                if (result.errors.length > 3) {
                    setTimeout(() => {
                        toast.info("Có thêm lỗi khác", {
                            description: `Và ${result.errors.length - 3} lỗi khác. Kiểm tra console để xem chi tiết.`,
                        })
                    }, 4000)
                }
            }

        } catch (error) {
            console.error('Error processing batch Excel data:', error)
            const errorMessage = error instanceof Error
                ? error.message
                : 'Có lỗi không xác định xảy ra'

            toast.error("Xử lý dữ liệu thất bại", {
                description: `Lỗi kết nối: ${errorMessage}`,
            })

            setProcessResult({
                success: false,
                message: `Lỗi kết nối: ${errorMessage}`,
                processed_count: 0,
            })
        } finally {
            setIsProcessing(false)
        }
    }

    const clearFileData = () => {
        const fileCount = uploadedFiles.length

        setUploadedFiles([])
        setProcessResult(null)

        if (fileInputRef.current) {
            fileInputRef.current.value = ""
        }
        if (folderInputRef.current) {
            folderInputRef.current.value = ""
        }

        if (fileCount > 0) {
            toast.success("Đã xóa dữ liệu", {
                description: `Đã xóa ${fileCount} file đã tải lên`,
            })
        }
    }

    //! Export sample Excel
    // const downloadSample = () => {
    //     const sampleData = [
    //         { "Tên": "Nguyễn Văn A", "Tuổi": 25, "Email": "nguyenvana@example.com", "Số điện thoại": "0123456789" },
    //         { "Tên": "Trần Thị B", "Tuổi": 30, "Email": "tranthib@example.com", "Số điện thoại": "0987654321" },
    //         { "Tên": "Lê Văn C", "Tuổi": 28, "Email": "levanc@example.com", "Số điện thoại": "0345678901" }
    //     ]

    //     const ws = XLSX.utils.json_to_sheet(sampleData)
    //     const wb = XLSX.utils.book_new()
    //     XLSX.utils.book_append_sheet(wb, ws, "Mẫu dữ liệu")
    //     XLSX.writeFile(wb, "mau-du-lieu.xlsx")
    // }

    const features = [
        {
            icon: Plane,
            title: "Quản lý Máy bay",
            description: "Quản lý thông tin máy bay: mã máy bay, số ghế.",
            href: "/aircraft",
            color: "text-blue-600"
        },
        {
            icon: Route,
            title: "Quản lý Đường bay",
            description: "Quản lý các tuyến đường bay: tên, quốc gia, thời gian bay ...",
            href: "/airway",
            color: "text-green-600"
        },
    ]

    return (
        <div className="space-y-12">
            {/* Hero Section */}
            <div className="text-center space-y-6 py-12">
                <div className="space-y-4">
                    <div className="flex items-center justify-center space-x-3 mb-6">
                        <div className="p-3 bg-primary rounded-full">
                            <Plane className="h-8 w-8 text-primary-foreground" />
                        </div>
                        <h1 className="text-5xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                            Vina Entry Hub
                        </h1>
                    </div>

                    <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
                        Hệ thống quản lý thông tin hàng không hiện đại. Quản lý máy bay và đường bay một cách
                        hiệu quả với giao diện thân thiện và dễ sử dụng.
                    </p>
                </div>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {features.map((feature) => (
                    <Card key={feature.title} className="aviation-card group">
                        <CardHeader>
                            <div className="flex items-center space-x-3">
                                <div className={`p-2 rounded-lg bg-muted ${feature.color}`}>
                                    <feature.icon className="h-6 w-6" />
                                </div>
                                <CardTitle className="text-xl">{feature.title}</CardTitle>
                            </div>
                        </CardHeader>
                        <CardContent className="flex flex-col h-full">
                            <CardDescription className="text-base mb-4">
                                {feature.description}
                            </CardDescription>

                            <Button variant="ghost" size="sm" asChild className="w-fit group-hover:translate-x-1 transition-transform mt-auto">
                                <Link to={feature.href}>
                                    Truy cập
                                    <ArrowRight className="h-4 w-4 ml-2" />
                                </Link>
                            </Button>
                        </CardContent>
                    </Card>
                ))}
            </div>

            {/* Excel Import Section */}
            <div className="space-y-6 py-12">
                <div className="text-center">
                    <h2 className="text-3xl font-bold mb-4">Import và xử lý dữ liệu từ Excel</h2>
                    <p className="text-muted-foreground max-w-2xl mx-auto">
                        Tải lên file Excel chuyến bay để làm sạch, xử lý và làm giàu dữ liệu.
                    </p>
                </div>

                <Card className="max-w-4xl mx-auto">
                    <CardHeader>
                        <CardTitle className="flex items-center space-x-2">
                            <FileSpreadsheet className="h-5 w-5" />
                            <span>Tải lên file Excel</span>
                        </CardTitle>
                        <CardDescription>
                            Hỗ trợ định dạng .xlsx và .xls. Kéo thả file/thư mục hoặc click để chọn file/thư mục.
                        </CardDescription>
                    </CardHeader>

                    <CardContent className="space-y-4">
                        {/* Upload Area */}
                        <div
                            className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-8 text-center hover:border-primary/50 transition-colors cursor-pointer"
                            onDragOver={handleDragOver}
                            onDrop={handleDrop}
                        >
                            <input
                                ref={fileInputRef}
                                type="file"
                                accept=".xlsx,.xls"
                                onChange={handleFileUpload}
                                className="hidden"
                                multiple
                            />
                            <input
                                ref={folderInputRef}
                                type="file"
                                onChange={handleFolderUpload}
                                className="hidden"
                                {...({ webkitdirectory: "", directory: "" } as any)}
                            />

                            {isUploading ? (
                                <div className="space-y-2">
                                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
                                    <p>Đang xử lý file...</p>
                                </div>
                            ) : uploadedFiles.length > 0 ? (
                                <div className="space-y-4">
                                    <FileSpreadsheet className="h-12 w-12 text-green-600 mx-auto" />
                                    <div className="space-y-2">
                                        <p className="font-medium">
                                            {uploadedFiles.length} file đã được tải lên
                                        </p>
                                        <div className="max-h-32 overflow-y-auto space-y-1">
                                            {uploadedFiles.map((file, index) => (
                                                <div key={index} className="flex items-center justify-between text-sm bg-muted/50 rounded px-3 py-2">
                                                    <span className="font-medium truncate">{file.name}</span>
                                                    <div className="flex items-center space-x-2 text-muted-foreground">
                                                        <span>{file.size} rows</span>
                                                        <button
                                                            onClick={(e) => {
                                                                e.stopPropagation()
                                                                const fileName = file.name
                                                                setUploadedFiles(prev => prev.filter((_, i) => i !== index))
                                                                toast.info("Đã xóa file", {
                                                                    description: `Đã xóa file: ${fileName}`,
                                                                })
                                                            }}
                                                            className="text-red-500 hover:text-red-700 ml-2 text-lg leading-none"
                                                            title={`Xóa file ${file.name}`}
                                                        >
                                                            ×
                                                        </button>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                        <p className="text-sm text-muted-foreground">
                                            Tổng cộng: {uploadedFiles.reduce((sum, file) => sum + file.size, 0)} dòng dữ liệu
                                        </p>
                                    </div>
                                </div>
                            ) : (
                                <div className="space-y-4">
                                    <Upload className="h-12 w-12 text-muted-foreground mx-auto" />
                                    <div className="space-y-2">
                                        <p className="font-medium">Kéo thả file/thư mục Excel vào đây hoặc click để chọn</p>
                                        <p className="text-sm text-muted-foreground">
                                            Hỗ trợ file .xlsx và .xls (có thể chọn nhiều file hoặc thư mục)
                                        </p>
                                    </div>
                                    <div className="flex items-center justify-center space-x-4">
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            onClick={(e) => {
                                                e.stopPropagation()
                                                fileInputRef.current?.click()
                                            }}
                                            className="flex items-center space-x-2"
                                        >
                                            <FileSpreadsheet className="h-4 w-4" />
                                            <span>Chọn file</span>
                                        </Button>
                                        <Button
                                            variant="outline"
                                            size="sm"
                                            onClick={(e) => {
                                                e.stopPropagation()
                                                folderInputRef.current?.click()
                                            }}
                                            className="flex items-center space-x-2"
                                        >
                                            <Folder className="h-4 w-4" />
                                            <span>Chọn thư mục</span>
                                        </Button>
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Action Buttons */}
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 justify-center items-center space-x-4">
                            {uploadedFiles.length > 0 && (
                                <>
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={(e) => {
                                            e.stopPropagation()
                                            fileInputRef.current?.click()
                                        }}
                                        className="flex items-center space-x-2 w-full"
                                        disabled={isProcessing || uploadedFiles.length === 0}
                                    >
                                        <FileSpreadsheet className="h-4 w-4" />
                                        <span>Chọn file</span>
                                    </Button>
                                    <Button
                                        variant="outline"
                                        size="sm"
                                        onClick={(e) => {
                                            e.stopPropagation()
                                            folderInputRef.current?.click()
                                        }}
                                        className="flex items-center space-x-2 w-full"
                                        disabled={isProcessing || uploadedFiles.length === 0}
                                    >
                                        <Folder className="h-4 w-4" />
                                        <span>Chọn thư mục</span>
                                    </Button>
                                    <Button
                                        onClick={() => processBatchExcelData(uploadedFiles)}
                                        disabled={isProcessing || uploadedFiles.length === 0}
                                        className="bg-green-600 hover:bg-green-700 w-full"
                                    >
                                        {isProcessing ? (
                                            <>
                                                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                                                Đang xử lý...
                                            </>
                                        ) : (
                                            <>
                                                <CheckCircle className="h-4 w-4 mr-2" />
                                                Xử lý {uploadedFiles.length} file
                                            </>
                                        )}
                                    </Button>
                                    <Button
                                        variant="destructive"
                                        onClick={clearFileData}
                                        className="w-full"
                                        disabled={isProcessing || uploadedFiles.length === 0}
                                    >
                                        Xóa tất cả file
                                    </Button>
                                </>
                            )}
                        </div>

                        {/* Processing Result */}
                        {processResult && (
                            <div className={`p-6 rounded-lg space-y-4 ${processResult.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                                {/* Header */}
                                <div className="flex items-start space-x-3">
                                    {processResult.success ? (
                                        <CheckCircle className="h-6 w-6 text-green-600 mt-0.5 flex-shrink-0" />
                                    ) : (
                                        <AlertCircle className="h-6 w-6 text-red-600 mt-0.5 flex-shrink-0" />
                                    )}
                                    <div className="flex-1">
                                        <h4 className={`font-semibold text-lg ${processResult.success ? 'text-green-800' : 'text-red-800'}`}>
                                            Kết quả xử lý dữ liệu
                                        </h4>
                                        <p className={`text-sm ${processResult.success ? 'text-green-700' : 'text-red-700'}`}>
                                            {processResult.message}
                                        </p>
                                    </div>
                                </div>

                                {/* Processing Summary Statistics */}
                                {processResult.processing_summary && (
                                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mt-4">
                                        <div className="bg-white rounded-lg p-3 border">
                                            <div className="text-2xl font-bold text-blue-600">
                                                {processResult.processing_summary.raw_records || 0}
                                            </div>
                                            <div className="text-xs text-gray-600">
                                                Bản ghi gốc
                                            </div>
                                        </div>
                                        <div className="bg-white rounded-lg p-3 border">
                                            <div className="text-2xl font-bold text-green-600">
                                                {processResult.processing_summary.processed_records || 0}
                                            </div>
                                            <div className="text-xs text-gray-600">
                                                Bản ghi đã xử lý
                                            </div>
                                        </div>
                                        <div className="bg-white rounded-lg p-3 border">
                                            <div className="text-2xl font-bold text-red-600">
                                                {processResult.processing_summary.error_records || 0}
                                            </div>
                                            <div className="text-xs text-gray-600">
                                                Lỗi
                                            </div>
                                        </div>
                                        <div className="bg-white rounded-lg p-3 border">
                                            <div className="text-2xl font-bold text-orange-600">
                                                {processResult.processing_summary.missing_actypes || 0}
                                            </div>
                                            <div className="text-xs text-gray-600">
                                                Actypes thiếu
                                            </div>
                                        </div>
                                        <div className="bg-white rounded-lg p-3 border">
                                            <div className="text-2xl font-bold text-orange-600">
                                                {processResult.processing_summary.missing_routes || 0}
                                            </div>
                                            <div className="text-xs text-gray-600">
                                                Routes thiếu
                                            </div>
                                        </div>
                                        <div className="bg-white rounded-lg p-3 border">
                                            <div className="text-2xl font-bold text-gray-600">
                                                {processResult.processing_summary.imported_files || 0}
                                            </div>
                                            <div className="text-xs text-gray-600">
                                                Files đã import
                                            </div>
                                        </div>
                                    </div>
                                )}

                                {/* Basic Stats when no detailed summary */}
                                {!processResult.processing_summary && processResult.success && (
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                        {processResult.processed_files && (
                                            <div className="bg-white rounded-lg p-3 border">
                                                <div className="text-2xl font-bold text-blue-600">
                                                    {processResult.processed_files}
                                                </div>
                                                <div className="text-xs text-gray-600">
                                                    Files đã xử lý
                                                </div>
                                            </div>
                                        )}
                                        {processResult.total_rows && (
                                            <div className="bg-white rounded-lg p-3 border">
                                                <div className="text-2xl font-bold text-green-600">
                                                    {processResult.total_rows}
                                                </div>
                                                <div className="text-xs text-gray-600">
                                                    Tổng số dòng
                                                </div>
                                            </div>
                                        )}
                                        {processResult.skipped_files && (
                                            <div className="bg-white rounded-lg p-3 border">
                                                <div className="text-2xl font-bold text-yellow-600">
                                                    {processResult.skipped_files}
                                                </div>
                                                <div className="text-xs text-gray-600">
                                                    Files đã bỏ qua
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                )}

                                {/* File Details */}
                                {processResult.file_details && processResult.file_details.length > 0 && (
                                    <div className="mt-4">
                                        <h5 className="font-medium text-gray-800 mb-2">Chi tiết file đã xử lý:</h5>
                                        <div className="space-y-1 max-h-32 overflow-y-auto">
                                            {processResult.file_details.map((file, index) => (
                                                <div key={index} className="flex items-center justify-between text-sm bg-white rounded px-3 py-2 border">
                                                    <span className="font-medium truncate flex-1">{file.file_name}</span>
                                                    <div className="flex items-center space-x-2 text-gray-600">
                                                        {file.file_type && (
                                                            <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">
                                                                {file.file_type}
                                                            </span>
                                                        )}
                                                        <span>{file.rows} rows</span>
                                                    </div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {/* Errors Display */}
                                {processResult.errors && processResult.errors.length > 0 && (
                                    <div className="mt-4 p-4 bg-red-100 rounded-lg border border-red-300">
                                        <h5 className="font-medium text-red-800 mb-2">Lỗi xảy ra ({processResult.errors.length}):</h5>
                                        <div className="text-sm text-red-700 space-y-1 max-h-32 overflow-y-auto">
                                            {processResult.errors.slice(0, 5).map((error, index) => (
                                                <p key={index}>• {error}</p>
                                            ))}
                                            {processResult.errors.length > 5 && (
                                                <p className="font-medium">... và {processResult.errors.length - 5} lỗi khác</p>
                                            )}
                                        </div>
                                    </div>
                                )}
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* Data Preview */}
                {uploadedFiles.length > 0 && (
                    <div className="space-y-6">
                        {uploadedFiles.map((file, fileIndex) => (
                            <Card key={fileIndex} className="max-w-6xl mx-auto">
                                <CardHeader>
                                    <CardTitle>Dữ liệu từ file: {file.name}</CardTitle>
                                    <CardDescription>
                                        Hiển thị {file.data.length} dòng dữ liệu
                                    </CardDescription>
                                </CardHeader>
                                <CardContent>
                                    <div className="overflow-x-auto">
                                        <table className="w-full border-collapse border border-border">
                                            <thead>
                                                <tr className="bg-muted">
                                                    {Object.keys(file.data[0] || {}).map((key) => (
                                                        <th key={key} className="border border-border p-2 text-left font-medium">
                                                            {key}
                                                        </th>
                                                    ))}
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {file.data.slice(0, 10).map((row, index) => (
                                                    <tr key={index} className="hover:bg-muted/50">
                                                        {Object.values(row).map((value, cellIndex) => (
                                                            <td key={cellIndex} className="border border-border p-2">
                                                                {String(value)}
                                                            </td>
                                                        ))}
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>

                                        {file.data.length > 10 && (
                                            <p className="text-center text-muted-foreground mt-4">
                                                Hiển thị 10 dòng đầu tiên. Tổng cộng có {file.data.length} dòng dữ liệu trong file này.
                                            </p>
                                        )}
                                    </div>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}

export default Index
