import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
    ArrowLeft,
    FolderDown,
    Sparkles,
    CalendarIcon,
    Plus
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

interface CountryProps {
    id: number
    country: string
    region: string
    region_vnm: string
    two_letter_code: string
    three_letter_code: string
    created_at: string
    updated_at: string
}

interface CountryDraftProps {
    id: number
    country?: string
    region?: string
    region_vnm?: string
    two_letter_code?: string
    three_letter_code?: string
    created_at?: string
    updated_at?: string
}

const DimCountry = () => {
    const navigate = useNavigate()

    const [data, setData] = useState<CountryDraftProps[]>([])
    const [exportData, setExportData] = useState<CountryProps[]>([])
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<string | null>(null)
    const [edit, setEdit] = useState<boolean>(false)

    async function getCountries() {
        setLoading(true)

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/countries`)
            const result = await response.json()

            setExportData(result)
            setError(null)
        } catch (error) {
            setError("Tải dữ liệu thất bại!")
        } finally {
            setLoading(false)
        }
    }

    async function getCountryDrafts() {
        setLoading(true)

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/dim-countries`)
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
        getCountryDrafts()
        getCountries()
    }, [])

    const updateRow = (id: number, field: keyof CountryDraftProps, value: string | number) => {
        setData((prev) => prev.map((row) => {
            return row.id === id ? { ...row, [field]: value } : row;
        }))
        setEdit(true)
    }

    const addRow = () => {
        const newRow: CountryDraftProps = {
            id: data.length + 1,
            country: "",
            region: "",
            region_vnm: "",
            two_letter_code: "",
            three_letter_code: "",
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
            row.country &&
            row.country.trim() !== '' &&
            row.region &&
            row.region.trim() !== '' &&
            row.region_vnm &&
            row.region_vnm.trim() !== '' &&
            row.two_letter_code &&
            row.two_letter_code.trim() !== '' &&
            row.three_letter_code &&
            row.three_letter_code.trim() !== ''
        )

        if (validData.length === 0) {
            toast.error("Không có dữ liệu hợp lệ để lưu!", {
                description: "Vui lòng nhập ít nhất một quốc gia với thông tin đầy đủ.",
            })
            return
        }

        const processedData = validData.map(row => ({
            country: row.country?.trim(),
            region: row.region?.trim(),
            region_vnm: row.region_vnm?.trim(),
            two_letter_code: row.two_letter_code?.trim(),
            three_letter_code: row.three_letter_code?.trim(),
        }))

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/countries/bulk-create`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ country_refs: processedData })
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
            getCountryDrafts()
            toast.success("Dữ liệu quốc gia đã được lưu thành công!", {
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

        const filteredData = exportData.filter(country => {
            const updateDate = country.updated_at ? new Date(country.updated_at) : new Date(country.created_at);
            return updateDate >= start && updateDate <= end;
        })

        if (filteredData.length === 0) {
            toast.warning("Không có dữ liệu trong khoảng thời gian đã chọn!", {
                description: "Vui lòng chọn khoảng thời gian khác."
            })
            return
        }

        import("xlsx").then((XLSX) => {
            const excelData = filteredData.map(country => ({
                Id: country.id,
                "Country": country.country,
                "Region": country.region,
                "Region VNM": country.region_vnm,
                "Two Letter Code": country.two_letter_code,
                "Three Letter Code": country.three_letter_code,
                "Created At": format(new Date(country.created_at), "dd-MM-yyyy HH:mm:ss"),
                "Updated At": country.updated_at ? format(new Date(country.updated_at), "dd-MM-yyyy HH:mm:ss") : "",
            }))

            const ws = XLSX.utils.json_to_sheet(excelData)
            const wb = XLSX.utils.book_new()
            XLSX.utils.book_append_sheet(wb, ws, "Countries")

            if ((end.getTime() - start.getTime()) <= 24 * 60 * 60 * 1000) {
                const fileName = `countries_${format(start, "dd-MM-yyyy")}.xlsx`
                XLSX.writeFile(wb, fileName)
                return
            }

            const fileName = `countries_${format(start, "dd-MM-yyyy")}_to_${format(end, "dd-MM-yyyy")}.xlsx`
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
                                        Quốc Gia
                                    </th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide min-w-[100px]">
                                        Khu Vực (QT)
                                    </th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide min-w-[100px]">
                                        Khu Vực (VN)
                                    </th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide min-w-[100px]">
                                        Mã 2 Ký Tự
                                    </th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide min-w-[100px]">
                                        Mã 3 Ký Tự
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
                                                retry={() => getCountryDrafts()}
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
                                        key={row.id}
                                        className={`border-b border-slate-200/40 dark:border-slate-700/40 hover:bg-sky-200/35 dark:hover:bg-sky-800/30 transition-all duration-200 group ${index % 2 === 0 ? "bg-white/40 dark:bg-slate-900/40" : "bg-slate-50/20 dark:bg-slate-800/20"
                                            }`}
                                    >
                                        <td className="p-3">
                                            <Input
                                                value={row.country}
                                                onChange={(e) => updateRow(row.id, "country", e.target.value.toUpperCase())}
                                                onFocus={(e) => e.target.select()}
                                                className="border-1 bg-transparent p-2 h-auto focus-visible:ring-2 focus-visible:ring-blue-500/20 focus-visible:bg-white/60 dark:focus-visible:bg-slate-800/60 rounded-lg transition-all duration-200 hover:bg-slate-50/50 dark:hover:bg-slate-800/50 font-medium placeholder:text-slate-400 placeholder:font-medium placeholder:italic"
                                            />
                                        </td>
                                        <td className="p-3">
                                            <Input
                                                value={row.region || ''}
                                                onChange={(e) => updateRow(row.id, "region", e.target.value)}
                                                onFocus={(e) => e.target.select()}
                                                className="border-1 bg-transparent p-2 h-auto focus-visible:ring-2 focus-visible:ring-blue-500/20 focus-visible:bg-white/60 dark:focus-visible:bg-slate-800/60 rounded-lg transition-all duration-200 hover:bg-slate-50/50 dark:hover:bg-slate-800/50 placeholder:text-slate-400 placeholder:font-medium placeholder:italic"
                                            />
                                        </td>
                                        <td className="p-3">
                                            <Input
                                                value={row.region_vnm || ''}
                                                onChange={(e) => updateRow(row.id, "region_vnm", e.target.value)}
                                                onFocus={(e) => e.target.select()}
                                                className="border-1 bg-transparent p-2 h-auto focus-visible:ring-2 focus-visible:ring-blue-500/20 focus-visible:bg-white/60 dark:focus-visible:bg-slate-800/60 rounded-lg transition-all duration-200 hover:bg-slate-50/50 dark:hover:bg-slate-800/50 placeholder:text-slate-400 placeholder:font-medium placeholder:italic"
                                            />
                                        </td>
                                        <td className="p-3">
                                            <Input
                                                value={row.two_letter_code || ''}
                                                onChange={(e) => updateRow(row.id, "two_letter_code", e.target.value)}
                                                onFocus={(e) => e.target.select()}
                                                className="border-1 bg-transparent p-2 h-auto focus-visible:ring-2 focus-visible:ring-blue-500/20 focus-visible:bg-white/60 dark:focus-visible:bg-slate-800/60 rounded-lg transition-all duration-200 hover:bg-slate-50/50 dark:hover:bg-slate-800/50 placeholder:text-slate-400 placeholder:font-medium placeholder:italic"
                                            />
                                        </td>
                                        <td className="p-3">
                                            <Input
                                                value={row.three_letter_code || ''}
                                                onChange={(e) => updateRow(row.id, "three_letter_code", e.target.value)}
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
    )
}

export default DimCountry;
