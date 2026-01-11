import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
    ArrowLeft,
    Sparkles,
    Plus,
    FolderUp
} from "lucide-react"
import { toast } from "sonner"
import { useNavigate } from "react-router"
import Loading from "@/components/Loading"
import ErrorBanner from "@/components/errorBanner"
import { Label } from "@/components/ui/label"

interface AirlineDraftProps {
    id: number
    carrier?: string
    airline_nation?: string
    airlines_name?: string
    created_at?: string
    updated_at?: string
}

const DimAirline = () => {
    const navigate = useNavigate()

    const [data, setData] = useState<AirlineDraftProps[]>([])
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<string | null>(null)
    const [edit, setEdit] = useState<boolean>(false)

    async function getAirlineDrafts() {
        setLoading(true)

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/dim-airlines`)
            const result = await response.json()

            setData(result)
            setError(null)
        } catch (error) {
            setError("Tải dữ liệu thất bại!")
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        getAirlineDrafts()
    }, [])

    const updateRow = (id: number, field: keyof AirlineDraftProps, value: string | number) => {
        setData((prev) => prev.map((row) => {
            return row.id === id ? { ...row, [field]: value } : row;
        }))
        setEdit(true)
    }

    const addRow = () => {
        const newRow: AirlineDraftProps = {
            id: data.length + 1,
            carrier: "",
            airline_nation: "",
            airlines_name: "",
        }
        setData((prev) => [...prev, newRow])
        setEdit(true)

        toast.success("Đã thêm hàng mới!", {
            description: "Vui lòng điền thông tin cho hàng mới."
        })
    }

    const handleSubmit = async () => {
        // Xử lý dữ liệu trước khi gửi
        const validData = data.filter(row =>
            (row.carrier && row.carrier.trim() !== '') ||
            (row.airline_nation && row.airline_nation.trim() !== '') ||
            (row.airlines_name && row.airlines_name.trim() !== '')
        )

        if (validData.length === 0) {
            toast.error("Không có dữ liệu hợp lệ để lưu!", {
                description: "Vui lòng nhập ít nhất một hãng hàng không với thông tin đầy đủ.",
            })
            return
        }

        const processedData = validData.map(row => ({
            carrier: row.carrier?.trim(),
            airline_nation: row.airline_nation?.trim(),
            airlines_name: row.airlines_name?.trim()
        }))

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/airlines/bulk-create`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ airline_refs: processedData })
            })

            if (!response.ok) {
                const errorData = await response.json()
                toast.error(errorData.detail, {
                    description: errorData.errors[0].message || "Có lỗi xảy ra khi lưu dữ liệu.",
                })
                return
            }

            setEdit(false)
            setLoading(false)
            setError(null)
            getAirlineDrafts()
            toast.success("Dữ liệu hãng hàng không đã được lưu thành công!", {
                description: "Tất cả thông tin đã được cập nhật trong cơ sở dữ liệu."
            })
        } catch (error) {
            toast.error("Lưu dữ liệu thất bại!", {
                description: "Có lỗi xảy ra khi lưu dữ liệu. Vui lòng thử lại.",
            })
        }
    }

    const handleBack = () => {
        if (edit) {
            toast.warning("Có thay đổi chưa lưu!", {
                description: "Rời khỏi trang?",
                duration: Infinity,
                closeButton: true,
                action: {
                    label: "Rời khỏi",
                    onClick: () => {
                        navigate("/")
                        toast.dismiss()
                    }
                },
                cancel: {
                    label: "Không, Ở lại",
                    onClick: () => {
                        toast.dismiss()
                    }
                },
            })
        } else {
            navigate("/")
        }
    }

    const handleImport = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0]
        if (!file) return

        const reader = new FileReader()
        reader.onload = async (event) => {
            const XLSX = await import("xlsx")
            const data = new Uint8Array(event.target?.result as ArrayBuffer)
            const workbook = XLSX.read(data, { type: 'array' })
            const sheetName = workbook.SheetNames[0]
            const worksheet = workbook.Sheets[sheetName]
            const json = XLSX.utils.sheet_to_json(worksheet, { header: 1 })

            const airlines = json.slice(1).map((row: any, index: number) => {
                return {
                    id: index + 1,
                    carrier: row[1],
                    airlines_name: row[2],
                    airline_nation: row[3],
                }
            })

            setData(airlines)
            setEdit(true)
        }
        reader.readAsArrayBuffer(file)
    }

    return (
        <div className="min-h-screen">
            <div className="p-8 max-w-7xl mx-auto">
                <h1 className="text-2xl font-bold text-center mb-10">Nhập Dữ Liệu Hãng Hàng Không</h1>

                <div className="mb-8 flex justify-center md:justify-between items-center">
                    <Button
                        variant="outline"
                        onClick={handleBack}
                        className="hidden md:flex items-center gap-2 hover:bg-white/80 dark:hover:bg-slate-800/80 transition-all duration-200 rounded-xl px-4 py-2"
                    >
                        <ArrowLeft className="h-4 w-4" />
                        Quay Lại
                    </Button>

                    <div>
                        <Label htmlFor="import-file" className="flex items-center gap-2 hover:bg-white/80 dark:hover:bg-slate-800/80 transition-all duration-200 rounded-xl px-4 py-2 cursor-pointer">
                            <FolderUp />
                            <span>Import</span>
                        </Label>
                        <Input
                            id="import-file"
                            name="import-file"
                            type="file"
                            onChange={handleImport}
                            accept=".xlsx,.xls,.csv"
                            className="hidden"
                        />
                    </div>
                </div>

                <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-2xl border border-slate-400 shadow-xl shadow-slate-200/20 dark:shadow-slate-900/20 overflow-hidden">
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-slate-400 bg-slate-300/30 dark:bg-slate-800/50">
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide min-w-[100px]">
                                        Mã Hãng
                                    </th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide min-w-[100px]">
                                        Tên Hãng
                                    </th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide min-w-[100px]">
                                        Quốc Gia
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                {loading ? (
                                    <tr>
                                        <td colSpan={3} className="py-6 text-center">
                                            <Loading />
                                        </td>
                                    </tr>
                                ) : error ? (
                                    <tr>
                                        <td colSpan={3}>
                                            <ErrorBanner
                                                title={error}
                                                description="Có lỗi xảy ra khi tải dữ liệu. Vui lòng thử lại."
                                                retry={() => getAirlineDrafts()}
                                            />
                                        </td>
                                    </tr>
                                ) : data.length === 0 ? (
                                    <tr>
                                        <td colSpan={3} className="p-3 text-center text-slate-500">
                                            Không có dữ liệu
                                        </td>
                                    </tr>
                                ) : data.map((row, index) => (
                                    <tr
                                        key={row.id}
                                        className={`border-b border-slate-200/40 dark:border-slate-700/40 hover:bg-sky-200/35 dark:hover:bg-sky-800/30 transition-all duration-200 group ${index % 2 === 0 ? "bg-white/40 dark:bg-slate-900/40" : "bg-slate-50/20 dark:bg-slate-800/20"
                                            }`}
                                    >
                                        <td className="p-3">
                                            <Input
                                                value={row.carrier}
                                                onChange={(e) => updateRow(row.id, "carrier", e.target.value.toUpperCase())}
                                                onFocus={(e) => e.target.select()}
                                                className="border-1 bg-transparent p-2 h-auto focus-visible:ring-2 focus-visible:ring-blue-500/20 focus-visible:bg-white/60 dark:focus-visible:bg-slate-800/60 rounded-lg transition-all duration-200 hover:bg-slate-50/50 dark:hover:bg-slate-800/50 font-medium placeholder:text-slate-400 placeholder:font-medium placeholder:italic"
                                            />
                                        </td>
                                        <td className="p-3">
                                            <Input
                                                value={row.airlines_name || ''}
                                                onChange={(e) => updateRow(row.id, "airlines_name", e.target.value)}
                                                onFocus={(e) => e.target.select()}
                                                className="border-1 bg-transparent p-2 h-auto focus-visible:ring-2 focus-visible:ring-blue-500/20 focus-visible:bg-white/60 dark:focus-visible:bg-slate-800/60 rounded-lg transition-all duration-200 hover:bg-slate-50/50 dark:hover:bg-slate-800/50 placeholder:text-slate-400 placeholder:font-medium placeholder:italic"
                                            />
                                        </td>
                                        <td className="p-3">
                                            <Input
                                                value={row.airline_nation || ''}
                                                onChange={(e) => updateRow(row.id, "airline_nation", e.target.value)}
                                                onFocus={(e) => e.target.select()}
                                                className="border-1 bg-transparent p-2 h-auto focus-visible:ring-2 focus-visible:ring-blue-500/20 focus-visible:bg-white/60 dark:focus-visible:bg-slate-800/60 rounded-lg transition-all duration-200 hover:bg-slate-50/50 dark:hover:bg-slate-800/50 placeholder:text-slate-400 placeholder:font-medium placeholder:italic"
                                            />
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div className="flex justify-between gap-4 mt-8">
                    <Button
                        onClick={addRow}
                        variant="outline"
                        className="border-green-500 text-green-600 hover:bg-green-50 dark:hover:bg-green-900/20 shadow-lg shadow-green-500/15 transition-all duration-200 rounded-xl px-6 py-2 flex items-center gap-2"
                    >
                        <Plus className="h-4 w-4" />
                        Thêm Hàng
                    </Button>

                    <Button
                        onClick={handleSubmit}
                        className="bg-primary text-primary-foreground shadow-lg shadow-blue-500/25 transition-all duration-200 rounded-xl px-6 py-2 flex items-center gap-2"
                    >
                        <Sparkles className="h-4 w-4" />
                        Lưu Dữ Liệu
                    </Button>
                </div>
            </div>
        </div>
    );
};

export default DimAirline;


