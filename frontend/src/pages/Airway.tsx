import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
    ArrowLeft,
    FolderDown,
    Sparkles,
    CalendarIcon
} from "lucide-react"
import { toast } from "sonner"
import { useNavigate } from "react-router"
import Loading from "@/components/Loading"
import ErrorBanner from "@/components/errorBanner"
import {
    CalendarCell,
    CalendarGrid,
    CalendarGridBody,
    CalendarGridHeader,
    CalendarHeaderCell,
    CalendarHeading,
    RangeCalendar,
} from "@/components/ui/calendar"
import {
    DatePickerContent,
    DateRangePicker,
} from "@/components/ui/date-range-picker"
import { DateInput } from "@/components/ui/datefield"
import { FieldGroup } from "@/components/ui/field"
import { AsiaButton } from "@/components/ui/asia-button"
import { format } from "date-fns"

interface RouteProps {
    index: number
    route: string
    ac?: string
    route_id?: string
    fh_theo_gio?: string
    flight_hour?: number
    taxi?: number
    block_hour?: number
    distance_km?: number
    loai?: string
    type?: string
    country?: string
    created_at: string
    updated_at: string
}

interface RouteDraftProps {
    route: string
    ac?: string
    route_id?: string
    fh_theo_gio?: number
    flight_hour?: number
    taxi?: number
    block_hour?: number
    distance_km?: number
    loai?: string
    type?: string
    country?: string
    created_at: string
}

const Airway = () => {
    const navigate = useNavigate()

    const [data, setData] = useState<RouteDraftProps[]>([])
    const [exportData, setExportData] = useState<RouteProps[]>([])
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<string | null>(null)
    const [edit, setEdit] = useState<boolean>(false)

    async function getRoutes() {
        setLoading(true)

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/routes`)
            const result = await response.json()

            setExportData(result)
            setError(null)
        } catch (error) {
            setError("Tải dữ liệu thất bại!")
        } finally {
            setLoading(false)
        }
    }

    async function getRouteDrafts() {
        setLoading(true)

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/temp-route-import`)
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
        getRouteDrafts()
        getRoutes()
    }, [])

    const updateRow = (route: string, field: keyof RouteDraftProps, value: string | number) => {
        setData((prev) => prev.map((row) => (row.route === route ? { ...row, [field]: value } : row)))
        setEdit(true)
    }

    const handleSubmit = async () => {
        // Xử lý dữ liệu trước khi gửi
        const validData = data.filter(row =>
            row.route &&
            row.route.trim() !== '' &&
            row.ac &&
            row.ac.trim() !== '' &&
            row.flight_hour &&
            row.flight_hour > 0 &&
            row.distance_km &&
            row.distance_km > 0 &&
            row.country &&
            row.country.trim() !== ''
        )

        if (validData.length === 0) {
            toast.error("Không có dữ liệu hợp lệ để lưu!", {
                description: "Vui lòng nhập ít nhất một tuyến bay với thông tin đầy đủ.",
            })
            return
        }

        const processedData = validData.map(row => ({
            route: row.route.trim(),
            ac: row.ac?.trim(),
            route_id: row.route_id?.trim() || null,
            flight_hour: row.flight_hour,
            fh_theo_gio: row.flight_hour,
            taxi: row?.taxi || null,
            block_hour: row?.block_hour || null,
            distance_km: row.distance_km,
            loai: row.loai?.trim() || null,
            type: row.type?.trim() || null,
            country: row.country?.trim(),
        }))

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/routes/bulk-create`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ routes: processedData })
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
            getRouteDrafts()
            toast.success("Dữ liệu tuyến bay đã được lưu thành công!", {
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

    const handleExport = () => {
        const hiddenInputs = document.querySelectorAll('input.react-aria-Input[hidden][type="text"]');

        const startValue = (hiddenInputs[0] as HTMLInputElement)?.value || null
        const endValue = (hiddenInputs[1] as HTMLInputElement)?.value || null

        if (!startValue || !endValue) {
            toast.error("Vui lòng chọn khoảng thời gian để xuất dữ liệu!", {
                description: "Chọn ngày bắt đầu và ngày kết thúc."
            })
            return
        }

        const start = new Date(startValue)
        const end = new Date(endValue)

        // Set giờ về 00:00:00.000 cho start và 23:59:59.999 cho end để bao gồm toàn bộ ngày
        start.setHours(0, 0, 0, 0)
        end.setHours(23, 59, 59, 999)

        const filteredData = exportData.filter(route => {
            return new Date(route.updated_at || route.created_at) >= start && new Date(route.updated_at || route.created_at) <= end;
        })

        if (filteredData.length === 0) {
            toast.warning("Không có dữ liệu trong khoảng thời gian đã chọn!", {
                description: "Vui lòng chọn khoảng thời gian khác."
            })
            return
        }

        import("xlsx").then((XLSX) => {
            const excelData = filteredData.map(route => ({
                Index: route.index,
                "Route Code": route.route,
                "Aircraft Type": route.ac,
                "Route ID": route.route_id,
                "Flight Hour": route.flight_hour,
                "Taxi Time": route.taxi,
                "Block Hour": route.block_hour,
                "Distance (km)": route.distance_km,
                "Type (VN)": route.loai,
                "Type (EN)": route.type,
                Country: route.country,
                "Created At": format(new Date(route.created_at), "dd-MM-yyyy HH:mm:ss"),
                "Updated At": route.updated_at ? format(new Date(route.updated_at), "dd-MM-yyyy HH:mm:ss") : "",
            }))

            const ws = XLSX.utils.json_to_sheet(excelData)
            const wb = XLSX.utils.book_new()
            XLSX.utils.book_append_sheet(wb, ws, "Routes")

            const fileName = `routes_export_${format(start, "dd-MM-yyyy")}_to_${format(end, "dd-MM-yyyy")}.xlsx`
            XLSX.writeFile(wb, fileName)
        })
    }

    return (
        <div className="min-h-screen">
            <div className="p-8 max-w-7xl mx-auto">
                <div className="mb-8 flex justify-center md:justify-between items-center">
                    <Button
                        variant="outline"
                        onClick={handleBack}
                        className="hidden md:flex items-center gap-2 hover:bg-white/80 dark:hover:bg-slate-800/80 transition-all duration-200 rounded-xl px-4 py-2"
                    >
                        <ArrowLeft className="h-4 w-4" />
                        Quay Lại
                    </Button>

                    <div className="flex flex-col sm:flex-row justify-between items-center gap-4 w-full md:w-auto">
                        <DateRangePicker className="min-w-[300px] space-y-1">
                            <FieldGroup>
                                <DateInput variant="ghost" slot={"start"} />
                                <span aria-hidden className="px-2 text-sm text-muted-foreground">
                                    -
                                </span>
                                <DateInput className="flex-1" variant="ghost" slot={"end"} />

                                <AsiaButton
                                    variant="ghost"
                                    size="icon"
                                    className="mr-1 size-6 data-[focus-visible]:ring-offset-0"
                                >
                                    <CalendarIcon aria-hidden className="size-4" />
                                </AsiaButton>
                            </FieldGroup>

                            <DatePickerContent>
                                <RangeCalendar>
                                    <CalendarHeading />
                                    <CalendarGrid>
                                        <CalendarGridHeader>
                                            {(day) => <CalendarHeaderCell>{day}</CalendarHeaderCell>}
                                        </CalendarGridHeader>
                                        <CalendarGridBody>
                                            {(date) => <CalendarCell date={date} />}
                                        </CalendarGridBody>
                                    </CalendarGrid>
                                </RangeCalendar>
                            </DatePickerContent>
                        </DateRangePicker>

                        <Button
                            variant="ghost"
                            onClick={handleExport}
                        >
                            <FolderDown />
                            <span>Export</span>
                        </Button>
                    </div>
                </div>

                <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-2xl border border-slate-400 shadow-xl shadow-slate-200/20 dark:shadow-slate-900/20 overflow-hidden">
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-slate-400 bg-slate-300/30 dark:bg-slate-800/50">
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide min-w-[100px]">
                                        Mã Tuyến Bay
                                    </th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide min-w-[100px]">
                                        Loại Máy Bay
                                    </th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide min-w-[100px]">
                                        Quốc Gia
                                    </th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide min-w-[100px]">
                                        Thời Gian Bay (giờ)
                                    </th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide min-w-[100px]">
                                        Khoảng Cách (km)
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                {loading ? (
                                    <tr>
                                        <td colSpan={5} className="py-6 text-center">
                                            <Loading />
                                        </td>
                                    </tr>
                                ) : error ? (
                                    <tr>
                                        <td colSpan={5}>
                                            <ErrorBanner
                                                title={error}
                                                description="Có lỗi xảy ra khi tải dữ liệu. Vui lòng thử lại."
                                                retry={() => getRouteDrafts()}
                                            />
                                        </td>
                                    </tr>
                                ) : data.length === 0 ? (
                                    <tr>
                                        <td colSpan={5} className="p-3 text-center text-slate-500">
                                            Không có dữ liệu
                                        </td>
                                    </tr>
                                ) : data.map((row, index) => (
                                    <tr
                                        key={row.route}
                                        className={`border-b border-slate-200/40 dark:border-slate-700/40 hover:bg-sky-200/35 dark:hover:bg-sky-800/30 transition-all duration-200 group ${index % 2 === 0 ? "bg-white/40 dark:bg-slate-900/40" : "bg-slate-50/20 dark:bg-slate-800/20"
                                            }`}
                                    >
                                        <td className="p-4">
                                            <Input
                                                value={row.route}
                                                onChange={(e) => updateRow(row.route, "route", e.target.value.toUpperCase())}
                                                onFocus={(e) => e.target.select()}
                                                className="border-0 bg-transparent p-2 h-auto focus-visible:ring-2 focus-visible:ring-blue-500/20 focus-visible:bg-white/60 dark:focus-visible:bg-slate-800/60 rounded-lg transition-all duration-200 hover:bg-slate-50/50 dark:hover:bg-slate-800/50 font-medium placeholder:text-slate-400 placeholder:font-medium placeholder:italic"
                                                placeholder="VD: HAN-SGN"
                                                tabIndex={-1}
                                            />
                                        </td>
                                        <td className="p-4">
                                            <Input
                                                value={row.ac || ''}
                                                onChange={(e) => updateRow(row.route, "ac", e.target.value.toUpperCase())}
                                                onFocus={(e) => e.target.select()}
                                                className="border-0 bg-transparent p-2 h-auto focus-visible:ring-2 focus-visible:ring-blue-500/20 focus-visible:bg-white/60 dark:focus-visible:bg-slate-800/60 rounded-lg transition-all duration-200 hover:bg-slate-50/50 dark:hover:bg-slate-800/50 placeholder:text-slate-400 placeholder:font-medium placeholder:italic"
                                                placeholder="A320"
                                            />
                                        </td>
                                        <td className="p-4">
                                            <Input
                                                value={row.country || ''}
                                                onChange={(e) => updateRow(row.route, "country", e.target.value)}
                                                onFocus={(e) => e.target.select()}
                                                className="border-0 bg-transparent p-2 h-auto focus-visible:ring-2 focus-visible:ring-blue-500/20 focus-visible:bg-white/60 dark:focus-visible:bg-slate-800/60 rounded-lg transition-all duration-200 hover:bg-slate-50/50 dark:hover:bg-slate-800/50 placeholder:text-slate-400 placeholder:font-medium placeholder:italic"
                                                placeholder="Việt Nam"
                                            />
                                        </td>
                                        <td className="p-4">
                                            <Input
                                                type="number"
                                                min={0}
                                                step="0.1"
                                                value={row.flight_hour || ''}
                                                onChange={(e) => updateRow(row.route, "flight_hour", parseFloat(e.target.value) || 0)}
                                                onFocus={(e) => e.target.select()}
                                                className="border-0 bg-transparent p-2 h-auto focus-visible:ring-2 focus-visible:ring-blue-500/20 focus-visible:bg-white/60 dark:focus-visible:bg-slate-800/60 rounded-lg transition-all duration-200 hover:bg-slate-50/50 dark:hover:bg-slate-800/50 placeholder:text-slate-400 placeholder:font-medium placeholder:italic"
                                                placeholder="2.5"
                                            />
                                        </td>
                                        <td className="p-4">
                                            <Input
                                                type="number"
                                                min={0}
                                                step="0.1"
                                                value={row.distance_km || ''}
                                                onChange={(e) => updateRow(row.route, "distance_km", parseFloat(e.target.value) || 0)}
                                                onFocus={(e) => e.target.select()}
                                                className="border-0 bg-transparent p-2 h-auto focus-visible:ring-2 focus-visible:ring-blue-500/20 focus-visible:bg-white/60 dark:focus-visible:bg-slate-800/60 rounded-lg transition-all duration-200 hover:bg-slate-50/50 dark:hover:bg-slate-800/50 placeholder:text-slate-400 placeholder:font-medium placeholder:italic"
                                                placeholder="1000"
                                            />
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div className="flex justify-end gap-4 mt-8">
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
    )
}

export default Airway;
