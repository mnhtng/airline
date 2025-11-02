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
    Folder,
    Building2,
    Landmark,
    Globe2,
    Download,
    Database,
    MapPin
} from "lucide-react"
import { useState, useRef } from "react"
import { toast } from "sonner"
import { JollyDateRangePicker } from "@/components/ui/date-range-picker"
import { today, getLocalTimeZone } from "@internationalized/date"
import { format } from "date-fns"
import type { DateRange } from "react-aria-components"

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

interface FlightExportData {
    area: string
    convert_date: string
    flightno: string
    route: string
    actype: string
    totalpax: number
    cgo: number
    mail: number
    acregno: string
    source: string
    sheet_name: string
    seat: string
    int_dom: string
    airline_code: string
    airlines_name: string
    airline_nation: string
    airline_nation_code: string
    departure: string
    city_departure: string
    country_departure: string
    arrives: string
    city_arrives: string
    country_arrives: string
    country_code: string
    area_code: string
    flight_type: number | string
}

interface ExportFlightDataResponse {
    success: boolean
    message: string
    data: FlightExportData[]
    total_records: number
}

interface APIErrorResponse {
    detail: string
}

const Index = () => {
    const [uploadedFiles, setUploadedFiles] = useState<ExcelFile[]>([])
    const [isUploading, setIsUploading] = useState(false)
    const [isProcessing, setIsProcessing] = useState(false)
    const [processResult, setProcessResult] = useState<ProcessResult | null>(null)

    // Reference input file to trigger programmatically
    const fileInputRef = useRef<HTMLInputElement>(null)
    const folderInputRef = useRef<HTMLInputElement>(null)

    // Export section states
    const [dateRange, setDateRange] = useState<DateRange | null>(null)
    const [isExporting, setIsExporting] = useState(false)

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

    const handleFolderUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const files = Array.from(event.target.files || [])
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
            reader.onload = async (e) => {
                try {
                    const XLSX = await import("xlsx")
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

            console.log(result)

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

    /**
     * Export flight data to Excel based on date range
     */
    const handleExportFlightData = async () => {
        if (!dateRange || !dateRange.start || !dateRange.end) {
            toast.warning("Vui lòng chọn khoảng thời gian", {
                description: "Chọn ngày bắt đầu và ngày kết thúc để xuất dữ liệu.",
            })
            return
        }

        setIsExporting(true)

        try {
            const startDate = new Date(
                dateRange.start.year,
                dateRange.start.month - 1, // month is 0-indexed in JavaScript
                dateRange.start.day
            )
            const endDate = new Date(
                dateRange.end.year,
                dateRange.end.month - 1,
                dateRange.end.day,
                23,
                59,
                59
            )

            // Format dates for API call
            const startDateStr = format(startDate, "yyyy-MM-dd HH:mm:ss")
            const endDateStr = format(endDate, "yyyy-MM-dd HH:mm:ss")

            // Encode URL parameters (for spaces and special characters)
            const encodedStartDate = encodeURIComponent(startDateStr)
            const encodedEndDate = encodeURIComponent(endDateStr)

            const response = await fetch(
                `${import.meta.env.VITE_API_URL}/data-processing/export-flight-data?start_date=${encodedStartDate}&end_date=${encodedEndDate}`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }
            )

            if (!response.ok) {
                const errorData = await response.json() as APIErrorResponse
                toast.error("Lỗi khi xuất dữ liệu", {
                    description: errorData.detail,
                })
                return
            }

            // Parse JSON response
            let result: ExportFlightDataResponse
            try {
                result = await response.json() as ExportFlightDataResponse
            } catch (parseError) {
                toast.error("Lỗi khi xử lý dữ liệu", {
                    description: "Phản hồi từ server không hợp lệ.",
                })
                return
            }

            // Handle unsuccessful response
            if (!result.success) {
                const message = result.message || "Có lỗi xảy ra khi xuất dữ liệu."
                toast.warning("Không thể xuất dữ liệu", {
                    description: message,
                })
                return
            }

            // Handle empty data
            if (!result.data || !Array.isArray(result.data) || result.data.length === 0) {
                const message = result.message || "Không có dữ liệu chuyến bay trong khoảng thời gian đã chọn."
                toast.warning("Không có dữ liệu", {
                    description: message,
                })
                return
            }

            // Export to Excel
            const XLSX = await import("xlsx")
            const excelData = result.data.map((flight: FlightExportData, index: number) => ({
                STT: index + 1,
                "Area": flight.area || "",
                "Convert Date": flight.convert_date || "",
                "Flight No": flight.flightno || "",
                "Route": flight.route || "",
                "Aircraft Type": flight.actype || "",
                "Total Pax": flight.totalpax || 0,
                "Cargo": flight.cgo || 0,
                "Mail": flight.mail || 0,
                "Aircraft Registration": flight.acregno || "",
                "Source": flight.source || "",
                "Sheet Name": flight.sheet_name || "",
                "Seat": flight.seat || "",
                "Int/Dom": flight.int_dom || "",
                "Airline Code": flight.airline_code || "",
                "Airlines Name": flight.airlines_name || "",
                "Airline Nation": flight.airline_nation || "",
                "Airline Nation Code": flight.airline_nation_code || "",
                "Departure": flight.departure || "",
                "City Departure": flight.city_departure || "",
                "Country Departure": flight.country_departure || "",
                "Arrives": flight.arrives || "",
                "City Arrives": flight.city_arrives || "",
                "Country Arrives": flight.country_arrives || "",
                "Country Code": flight.country_code || "",
                "Area Code": flight.area_code || "",
                "Flight Type": flight.flight_type !== "" ? flight.flight_type : "",
            }))

            const ws = XLSX.utils.json_to_sheet(excelData)
            const wb = XLSX.utils.book_new()
            XLSX.utils.book_append_sheet(wb, ws, "Flight Report")

            // Auto-fit column widths
            const maxWidth = 30
            const wscols = Object.keys(excelData[0] || {}).map(() => ({ wch: maxWidth }))
            ws['!cols'] = wscols

            // Generate filename based on date range
            let fileName: string
            if ((endDate.getTime() - startDate.getTime()) <= 24 * 60 * 60 * 1000) {
                fileName = `flight_report_${format(startDate, "dd-MM-yyyy")}.xlsx`
            } else {
                fileName = `flight_report_${format(startDate, "dd-MM-yyyy")}_to_${format(endDate, "dd-MM-yyyy")}.xlsx`
            }

            XLSX.writeFile(wb, fileName)
        } catch (error) {
            toast.error("Lỗi khi xuất dữ liệu", {
                description: error instanceof Error ? error.message : "Có lỗi không xác định xảy ra",
            })
        } finally {
            setIsExporting(false)
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
            title: "Máy bay",
            description: "Quản lý thông tin số ghế máy bay.",
            href: {
                dim: "/temp/aircraft",
                fact: "/manager/aircraft"
            },
            color: "text-blue-600"
        },
        {
            icon: Building2,
            title: "Hãng hàng không",
            description: "Quản lý thông tin hãng hàng không.",
            href: {
                dim: "/temp/airline",
                fact: "/manager/airline"
            },
            color: "text-purple-600"
        },
        {
            icon: Landmark,
            title: "Sân bay",
            description: "Quản lý thông tin sân bay.",
            href: {
                dim: "/temp/airport",
                fact: "/manager/airport"
            },
            color: "text-amber-600"
        },
        {
            icon: Globe2,
            title: "Quốc gia",
            description: "Quản lý thông tin quốc gia.",
            href: {
                dim: "/temp/country",
                fact: "/manager/country"
            },
            color: "text-cyan-600"
        },
        {
            icon: Route,
            title: "Tuyến bay",
            description: "Quản lý thông tin tuyến bay và phân loại đường bay.",
            href: {
                dim: "/temp/sector-route",
                fact: "/manager/sector-route"
            },
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
                            Sun Phu Quoc Airways
                        </h1>
                    </div>

                    <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
                        Hệ thống quản lý hàng không: máy bay, hãng, sân bay, quốc gia và phân loại đường bay.
                    </p>
                </div>
            </div>

            {/* Features Grid - Compact Design */}
            <div className="hidden lg:grid lg:grid-cols-3 xl:grid-cols-5 gap-4">
                {features.map((feature) => (
                    <Card key={feature.title} className="aviation-card group hover:shadow-lg transition-all duration-200 hover:scale-105">
                        <CardHeader className="pb-3">
                            <div className="flex flex-col items-center text-center space-y-3">
                                <div className={`p-3 rounded-full bg-muted ${feature.color} group-hover:scale-110 transition-transform duration-200`}>
                                    <feature.icon className="h-5 w-5" />
                                </div>
                                <CardTitle className="text-sm font-semibold leading-tight">{feature.title}</CardTitle>
                            </div>
                        </CardHeader>
                        <CardContent className="pt-0 pb-4 h-full flex flex-col justify-between">
                            <CardDescription className="text-xs text-center leading-relaxed mb-2">
                                {feature.description}
                            </CardDescription>

                            <div className="flex justify-evenly items-center gap-2">
                                <Button
                                    variant="ghost"
                                    size="sm"
                                    asChild
                                    className="text-xs group-hover:bg-primary/10 transition-all duration-200"
                                >
                                    <Link to={feature.href.dim} className="flex items-center justify-center space-x-1">
                                        <span>Phiếu điền</span>
                                        <ArrowRight className="h-3 w-3" />
                                    </Link>
                                </Button>

                                <Button
                                    variant="ghost"
                                    size="sm"
                                    asChild
                                    className="text-xs group-hover:bg-primary/10 transition-all duration-200"
                                >
                                    <Link to={feature.href.fact} className="flex items-center justify-center space-x-1">
                                        <span>Quản lý</span>
                                        <ArrowRight className="h-3 w-3" />
                                    </Link>
                                </Button>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            {/* Excel Import Section */}
            <div className="space-y-6 py-12">
                <div className="text-center">
                    <h2 className="text-3xl font-bold mb-4">
                        Import/Export dữ liệu chuyến bay
                    </h2>
                </div>

                {/* Export Flight Data Section */}
                <Card className="max-w-4xl mx-auto mt-8">
                    <CardHeader>
                        <CardTitle className="flex items-center space-x-2">
                            <Download className="h-5 w-5" />
                            <span>Xuất dữ liệu chuyến bay</span>
                        </CardTitle>
                        <CardDescription>
                            Chọn khoảng thời gian để xuất dữ liệu chuyến bay đã xử lý thành file Excel.
                        </CardDescription>
                    </CardHeader>

                    <CardContent className="space-y-6">
                        {/* Date Range Picker */}
                        <div className="flex flex-col space-y-4">
                            <JollyDateRangePicker
                                label="Chọn khoảng thời gian"
                                description="Chọn ngày bắt đầu và ngày kết thúc để xuất dữ liệu chuyến bay"
                                value={dateRange}
                                onChange={setDateRange}
                                maxValue={today(getLocalTimeZone())}
                                className="w-full"
                            />

                            {/* Export Statistics */}
                            {dateRange && dateRange.start && dateRange.end && (
                                <div className="bg-muted/50 rounded-lg p-4 space-y-2">
                                    <div className="flex items-center justify-between text-sm">
                                        <span className="text-muted-foreground">Từ ngày:</span>
                                        <span className="font-medium">
                                            {format(
                                                new Date(
                                                    dateRange.start.year,
                                                    dateRange.start.month - 1,
                                                    dateRange.start.day
                                                ),
                                                "dd/MM/yyyy"
                                            )}
                                        </span>
                                    </div>
                                    <div className="flex items-center justify-between text-sm">
                                        <span className="text-muted-foreground">Đến ngày:</span>
                                        <span className="font-medium">
                                            {format(
                                                new Date(
                                                    dateRange.end.year,
                                                    dateRange.end.month - 1,
                                                    dateRange.end.day
                                                ),
                                                "dd/MM/yyyy"
                                            )}
                                        </span>
                                    </div>
                                    <div className="flex items-center justify-between text-sm">
                                        <span className="text-muted-foreground">Số ngày:</span>
                                        <span className="font-medium">
                                            {Math.ceil(
                                                (new Date(
                                                    dateRange.end.year,
                                                    dateRange.end.month - 1,
                                                    dateRange.end.day
                                                ).getTime() -
                                                    new Date(
                                                        dateRange.start.year,
                                                        dateRange.start.month - 1,
                                                        dateRange.start.day
                                                    ).getTime()) /
                                                (1000 * 60 * 60 * 24)
                                            ) + 1} ngày
                                        </span>
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Export Button */}
                        <div className="flex justify-center">
                            <Button
                                onClick={handleExportFlightData}
                                disabled={isExporting || !dateRange || !dateRange.start || !dateRange.end}
                                className="bg-blue-600 hover:bg-blue-700 w-full md:w-auto"
                                size="lg"
                            >
                                {isExporting ? (
                                    <>
                                        <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                                        Đang xuất dữ liệu...
                                    </>
                                ) : (
                                    <>
                                        <Download className="h-5 w-5 mr-2" />
                                        Xuất dữ liệu chuyến bay
                                    </>
                                )}
                            </Button>
                        </div>
                    </CardContent>
                </Card>

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
                            <div className={`p-6 rounded-lg space-y-6 ${processResult.success ? 'bg-green-50 border-2 border-green-200' : 'bg-red-50 border-2 border-red-200'}`}>
                                {/* Header with Summary */}
                                <div className="flex items-start space-x-3 flex-1">
                                    {processResult.success ? (
                                        <CheckCircle className="h-7 w-7 text-green-600 mt-0.5 flex-shrink-0" />
                                    ) : (
                                        <AlertCircle className="h-7 w-7 text-red-600 mt-0.5 flex-shrink-0" />
                                    )}
                                    <div className="flex-1">
                                        <h4 className={`font-bold text-xl ${processResult.success ? 'text-green-800' : 'text-red-800'}`}>
                                            {processResult.success ? 'Xử lý dữ liệu thành công' : 'Xử lý dữ liệu thất bại'}
                                        </h4>
                                        <p className={`text-sm mt-1 ${processResult.success ? 'text-green-700' : 'text-red-700'}`}>
                                            {processResult.message}
                                        </p>
                                    </div>
                                </div>

                                {/* Processing Summary Statistics */}
                                {processResult.processing_summary && (
                                    <div className="space-y-4">
                                        <div className="flex items-center justify-between">
                                            <h5 className="font-semibold text-primary text-base">Thống kê chi tiết</h5>
                                            <div className="text-xs text-muted-foreground">
                                                {(() => {
                                                    const total = processResult.processing_summary.raw_records || 0
                                                    const processed = processResult.processing_summary.processed_records || 0
                                                    const successRate = total > 0 ? ((processed / total) * 100).toFixed(1) : '0'
                                                    return `Tỷ lệ thành công: ${successRate}%`
                                                })()
                                                }
                                            </div>
                                        </div>

                                        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
                                            {/* Raw Records */}
                                            <div className="bg-white rounded-lg p-4 border-2 border-blue-200 hover:shadow-md transition-shadow group relative">
                                                <div className="flex items-start justify-between mb-2">
                                                    <div className="p-2 bg-blue-100 rounded-lg">
                                                        <Database className="h-4 w-4 text-blue-600" />
                                                    </div>
                                                </div>

                                                <div className="text-2xl font-bold text-blue-600">
                                                    {processResult.processing_summary.raw_records?.toLocaleString() || 0}
                                                </div>
                                                <div className="text-xs text-gray-600 font-medium mt-1">
                                                    Bản ghi gốc
                                                </div>
                                                <div className="text-xs text-gray-500 mt-0.5">
                                                    flight_raw
                                                </div>
                                            </div>

                                            {/* Processed Records */}
                                            <div className="bg-white rounded-lg p-4 border-2 border-green-200 hover:shadow-md transition-shadow relative">
                                                <div className="flex items-start justify-between mb-2">
                                                    <div className="p-2 bg-green-100 rounded-lg">
                                                        <CheckCircle className="h-4 w-4 text-green-600" />
                                                    </div>
                                                </div>

                                                <div className="text-2xl font-bold text-green-600">
                                                    {processResult.processing_summary.processed_records?.toLocaleString() || 0}
                                                </div>
                                                <div className="text-xs text-gray-600 font-medium mt-1">
                                                    Đã xử lý
                                                </div>
                                                <div className="text-xs text-gray-500 mt-0.5">
                                                    {(() => {
                                                        const total = processResult.processing_summary.raw_records || 0
                                                        const processed = processResult.processing_summary.processed_records || 0
                                                        return total > 0 ? `${((processed / total) * 100).toFixed(1)}%` : '0%'
                                                    })()}
                                                </div>
                                            </div>

                                            {/* Error Records */}
                                            <div className="bg-white rounded-lg p-4 border-2 border-red-200 hover:shadow-md transition-shadow relative">
                                                <div className="flex items-start justify-between mb-2">
                                                    <div className="p-2 bg-red-100 rounded-lg">
                                                        <AlertCircle className="h-4 w-4 text-red-600" />
                                                    </div>
                                                </div>

                                                <div className="text-2xl font-bold text-red-600">
                                                    {processResult.processing_summary.error_records?.toLocaleString() || 0}
                                                </div>
                                                <div className="text-xs text-gray-600 font-medium mt-1">
                                                    Lỗi validation
                                                </div>
                                                <div className="text-xs text-gray-500 mt-0.5">
                                                    error_table
                                                </div>
                                            </div>

                                            {/* Missing Actypes */}
                                            <div className="bg-white rounded-lg p-4 border-2 border-orange-200 hover:shadow-md transition-shadow relative">
                                                <div className="flex items-start justify-between mb-2">
                                                    <div className="p-2 bg-orange-100 rounded-lg">
                                                        <Plane className="h-4 w-4 text-orange-600" />
                                                    </div>
                                                </div>

                                                <div className="text-2xl font-bold text-orange-600">
                                                    {processResult.processing_summary.missing_actypes?.toLocaleString() || 0}
                                                </div>
                                                <div className="text-xs text-gray-600 font-medium mt-1">
                                                    Actypes thiếu
                                                </div>
                                                <div className="text-xs text-gray-500 mt-0.5">
                                                    Cần bổ sung
                                                </div>
                                            </div>

                                            {/* Missing Routes */}
                                            <div className="bg-white rounded-lg p-4 border-2 border-orange-200 hover:shadow-md transition-shadow relative">
                                                <div className="flex items-start justify-between mb-2">
                                                    <div className="p-2 bg-orange-100 rounded-lg">
                                                        <MapPin className="h-4 w-4 text-orange-600" />
                                                    </div>
                                                </div>

                                                <div className="text-2xl font-bold text-orange-600">
                                                    {processResult.processing_summary.missing_routes?.toLocaleString() || 0}
                                                </div>
                                                <div className="text-xs text-gray-600 font-medium mt-1">
                                                    Routes thiếu
                                                </div>
                                                <div className="text-xs text-gray-500 mt-0.5">
                                                    Cần bổ sung
                                                </div>
                                            </div>

                                            {/* Imported Files */}
                                            <div className="bg-white rounded-lg p-4 border-2 border-purple-200 hover:shadow-md transition-shadow relative">
                                                <div className="flex items-start justify-between mb-2">
                                                    <div className="p-2 bg-purple-100 rounded-lg">
                                                        <FileSpreadsheet className="h-4 w-4 text-purple-600" />
                                                    </div>
                                                </div>

                                                <div className="text-2xl font-bold text-purple-600">
                                                    {processResult.processing_summary.imported_files?.toLocaleString() || 0}
                                                </div>
                                                <div className="text-xs text-gray-600 font-medium mt-1">
                                                    Files imported
                                                </div>
                                                <div className="text-xs text-gray-500 mt-0.5">
                                                    import_log
                                                </div>
                                            </div>
                                        </div>

                                        {/* Progress Bar */}
                                        <div className="bg-white rounded-lg p-4 border">
                                            <div className="flex items-center justify-between mb-2">
                                                <span className="text-sm font-medium text-gray-700">Tiến trình xử lý</span>
                                                <span className="text-sm font-semibold text-gray-900">
                                                    {(() => {
                                                        const total = processResult.processing_summary.raw_records || 0
                                                        const processed = processResult.processing_summary.processed_records || 0
                                                        return total > 0 ? `${((processed / total) * 100).toFixed(1)}%` : '0%'
                                                    })()}
                                                </span>
                                            </div>
                                            <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                                                <div
                                                    className="bg-gradient-to-r from-green-500 to-green-600 h-3 rounded-full transition-all duration-500 flex items-center justify-end pr-2"
                                                    style={{
                                                        width: `${(() => {
                                                            const total = processResult.processing_summary.raw_records || 0
                                                            const processed = processResult.processing_summary.processed_records || 0
                                                            return total > 0 ? (processed / total) * 100 : 0
                                                        })()}%`
                                                    }}
                                                >
                                                    {(() => {
                                                        const total = processResult.processing_summary.raw_records || 0
                                                        const processed = processResult.processing_summary.processed_records || 0
                                                        const percent = total > 0 ? (processed / total) * 100 : 0
                                                        return percent > 10 && (
                                                            <span className="text-xs font-bold text-white">✓</span>
                                                        )
                                                    })()}
                                                </div>
                                            </div>
                                            <div className="flex justify-between mt-2 text-xs text-gray-600">
                                                <span>✅ {processResult.processing_summary.processed_records?.toLocaleString() || 0} thành công</span>
                                                <span>❌ {processResult.processing_summary.error_records?.toLocaleString() || 0} lỗi</span>
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
