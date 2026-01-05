import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
    Plus,
    Edit,
    Trash,
    Loader,
    ChevronLeft,
    ChevronRight,
    ChevronsLeft,
    ChevronsRight,
    Search,
    FolderDown,
    CalendarIcon,
} from "lucide-react"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { toast } from "sonner"
import Loading from "@/components/Loading"
import ErrorBanner from "@/components/errorBanner"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
    DialogFooter,
    DialogClose,
} from "@/components/ui/dialog"
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { Label } from "@/components/ui/label"
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

interface Airline {
    id: number;
    carrier: string;
    airline_nation: string;
    airlines_name: string;
    created_at: string;
    updated_at: string;
}

const Airline = () => {
    const [data, setData] = useState<Airline[]>([])
    const [exportData, setExportData] = useState<Airline[]>([])
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<string | null>(null)
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [isAlertOpen, setIsAlertOpen] = useState(false);
    const [selectedAirline, setSelectedAirline] = useState<Airline | null>(null);
    const [formData, setFormData] = useState({ carrier: '', airline_nation: '', airlines_name: '' });
    const [formError, setFormError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(10);
    const [searchTerm, setSearchTerm] = useState("");


    async function getAirlines(search: string = "") {
        setLoading(true)
        try {
            const url = search
                ? `${import.meta.env.VITE_API_URL}/airlines/search/?q=${search}`
                : `${import.meta.env.VITE_API_URL}/airlines/`;
            const response = await fetch(url)
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            const result = await response.json()
            setData(result)
            setExportData(result)
            setError(null)
        } catch (error) {
            setError("Tải dữ liệu thất bại!")
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        const debounceTimer = setTimeout(() => {
            getAirlines(searchTerm);
        }, 500); // 500ms debounce delay

        return () => clearTimeout(debounceTimer);
    }, [searchTerm]);

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

        const filteredData = exportData.filter(airline => {
            const updateDate = airline.updated_at ? new Date(airline.updated_at) : new Date(airline.created_at);
            return updateDate >= start && updateDate <= end;
        })

        if (filteredData.length === 0) {
            toast.warning("Không có dữ liệu trong khoảng thời gian đã chọn!", {
                description: "Vui lòng chọn khoảng thời gian khác."
            })
            return
        }

        import("xlsx").then((XLSX) => {
            const excelData = filteredData.map((airline, index) => ({
                "STT": index + 1,
                "Mã Hãng": airline.carrier,
                "Tên Hãng": airline.airlines_name,
                "Quốc Gia": airline.airline_nation,
                "Ngày Tạo": format(new Date(airline.created_at), "yyyy-MM-dd HH:mm:ss"),
                "Ngày Cập Nhật": airline.updated_at ? format(new Date(airline.updated_at), "yyyy-MM-dd HH:mm:ss") : "",
            }))

            const ws = XLSX.utils.json_to_sheet(excelData)
            const wb = XLSX.utils.book_new()
            XLSX.utils.book_append_sheet(wb, ws, "Airlines")

            if ((end.getTime() - start.getTime()) <= 24 * 60 * 60 * 1000) {
                const fileName = `airlines_${format(start, "yyyy-MM-dd")}.xlsx`
                XLSX.writeFile(wb, fileName)
                return
            }

            const fileName = `airlines_${format(start, "yyyy-MM-dd")}_to_${format(end, "yyyy-MM-dd")}.xlsx`
            XLSX.writeFile(wb, fileName)
        })
    }

    const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { id, value } = e.target;
        setFormData(prev => ({ ...prev, [id]: value }));
    };

    const validateForm = () => {
        if (!formData.carrier.trim()) {
            setFormError('Mã hãng không được để trống.');
            return false;
        }
        if (!formData.airline_nation.trim()) {
            setFormError('Quốc gia không được để trống.');
            return false;
        }
        if (!formData.airlines_name.trim()) {
            setFormError('Tên hãng hàng không không được để trống.');
            return false;
        }
        setFormError(null);
        return true;
    };

    const handleCreateOrUpdate = async () => {
        if (!validateForm()) return;

        setIsSubmitting(true);
        const method = selectedAirline ? "PUT" : "POST";
        const url = selectedAirline
            ? `${import.meta.env.VITE_API_URL}/airlines/${selectedAirline.id}`
            : `${import.meta.env.VITE_API_URL}/airlines/`;

        const body = {
            carrier: formData.carrier.trim().toUpperCase(),
            airline_nation: formData.airline_nation.trim(),
            airlines_name: formData.airlines_name.trim(),
        };

        try {
            const response = await fetch(url, {
                method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Có lỗi xảy ra");
            }

            toast.success(`Đã ${selectedAirline ? 'cập nhật' : 'tạo mới'} hãng hàng không thành công!`);
            setIsDialogOpen(false);
            getAirlines(); // Refresh data
        } catch (error: any) {
            toast.error(error.message || `Không thể ${selectedAirline ? 'cập nhật' : 'tạo mới'} hãng hàng không.`);
        } finally {
            setIsSubmitting(false);
        }
    };


    const handleDelete = async () => {
        if (!selectedAirline) return;

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/airlines/${selectedAirline.id}`, {
                method: "DELETE"
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Có lỗi xảy ra");
            }

            toast.success("Đã xóa hãng hàng không thành công!");
            setIsAlertOpen(false);
            getAirlines(); // Refresh data
        } catch (error: any) {
            toast.error(error.message || "Không thể xóa hãng hàng không.");
        }
    };


    const openDialog = (airline: Airline | null) => {
        setSelectedAirline(airline);
        setFormData(airline ? { carrier: airline.carrier, airline_nation: airline.airline_nation, airlines_name: airline.airlines_name } : { carrier: '', airline_nation: '', airlines_name: '' });
        setFormError(null);
        setIsDialogOpen(true);
    };

    const openAlertDialog = (airline: Airline) => {
        setSelectedAirline(airline);
        setIsAlertOpen(true);
    };

    // Pagination logic
    const totalPages = Math.ceil(data.length / itemsPerPage);
    const paginatedData = data.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

    const goToPage = (page: number) => {
        setCurrentPage(Math.max(1, Math.min(page, totalPages)));
    };

    const handleItemsPerPageChange = (value: string) => {
        setItemsPerPage(Number(value));
        setCurrentPage(1); // Reset to first page
    };


    return (
        <div className="min-h-screen">
            <div className="p-8 max-w-7xl mx-auto">
                <h1 className="text-2xl font-bold text-center mb-10">Quản Lý Hãng Hàng Không</h1>

                <div className="mb-8">
                    <div className="flex flex-col lg:flex-row justify-between items-center gap-5">
                        <div className="flex items-center gap-2">
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
                            </Button>
                        </div>
                        <div className="flex items-center gap-2 w-full lg:w-auto">
                            <div className="relative w-full">
                                <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                                <Input
                                    type="search"
                                    placeholder="Tìm kiếm hãng hàng không..."
                                    className="pl-8 lg:w-[300px]"
                                    value={searchTerm}
                                    onChange={(e) => setSearchTerm(e.target.value)}
                                />
                            </div>
                            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                                <DialogTrigger asChild>
                                    <Button onClick={() => openDialog(null)} className="flex items-center gap-2">
                                        <Plus className="h-4 w-4" />
                                        Thêm
                                    </Button>
                                </DialogTrigger>
                                <DialogContent className="sm:max-w-[425px]">
                                    <DialogHeader>
                                        <DialogTitle>{selectedAirline ? "Chỉnh Sửa Hãng Hàng Không" : "Thêm Hãng Hàng Không Mới"}</DialogTitle>
                                        <DialogDescription>
                                            {selectedAirline ? "Cập nhật thông tin hãng hàng không." : "Điền thông tin để tạo hãng hàng không mới."}
                                        </DialogDescription>
                                    </DialogHeader>
                                    <div className="grid gap-4 py-4">
                                        <div className="grid grid-cols-4 items-center gap-4">
                                            <Label htmlFor="carrier" className="text-right">
                                                Mã Hãng
                                            </Label>
                                            <Input id="carrier" value={formData.carrier} onChange={handleFormChange} className="col-span-3" />
                                        </div>
                                        <div className="grid grid-cols-4 items-center gap-4">
                                            <Label htmlFor="airlines_name" className="text-right">
                                                Tên Hãng
                                            </Label>
                                            <Input id="airlines_name" value={formData.airlines_name} onChange={handleFormChange} className="col-span-3" />
                                        </div>
                                        <div className="grid grid-cols-4 items-center gap-4">
                                            <Label htmlFor="airline_nation" className="text-right">
                                                Quốc Gia
                                            </Label>
                                            <Input id="airline_nation" value={formData.airline_nation} onChange={handleFormChange} className="col-span-3" />
                                        </div>
                                        {formError && <p className="col-span-4 text-red-500 text-sm text-center">{formError}</p>}
                                    </div>
                                    <DialogFooter>
                                        <DialogClose asChild>
                                            <Button type="button" variant="secondary">Hủy</Button>
                                        </DialogClose>
                                        <Button onClick={handleCreateOrUpdate} disabled={isSubmitting}>
                                            {isSubmitting && <Loader className="mr-2 h-4 w-4 animate-spin" />}
                                            {selectedAirline ? "Lưu thay đổi" : "Tạo"}
                                        </Button>
                                    </DialogFooter>
                                </DialogContent>
                            </Dialog>
                        </div>
                    </div>
                </div>

                <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-2xl border border-slate-400 shadow-xl shadow-slate-200/20 dark:shadow-slate-900/20 overflow-hidden">
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-slate-400 bg-slate-300/30 dark:bg-slate-800/50">
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Mã Hãng</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Tên Hãng</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Quốc Gia</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Ngày Tạo</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Ngày Cập Nhật</th>
                                    <th className="text-right text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Hành Động</th>
                                </tr>
                            </thead>
                            <tbody>
                                {loading ? (
                                    <tr><td colSpan={6} className="py-6 text-center"><Loading /></td></tr>
                                ) : error ? (
                                    <tr><td colSpan={6}><ErrorBanner title={error} description="Có lỗi xảy ra khi tải dữ liệu. Vui lòng thử lại." retry={() => getAirlines(searchTerm)} /></td></tr>
                                ) : data.length === 0 ? (
                                    <tr><td colSpan={6} className="p-3 text-center text-slate-500">Không có dữ liệu</td></tr>
                                ) : paginatedData.map((item, index) => (
                                    <tr key={item.id} className={`border-b border-slate-200/40 dark:border-slate-700/40 hover:bg-sky-200/35 dark:hover:bg-sky-800/30 transition-all duration-200 group ${index % 2 === 0 ? "bg-white/40 dark:bg-slate-900/40" : "bg-slate-50/20 dark:bg-slate-800/20"}`}>
                                        <td className="p-3 font-medium">{item.carrier}</td>
                                        <td className="p-3">{item.airlines_name}</td>
                                        <td className="p-3">{item.airline_nation}</td>
                                        <td className="p-3">{new Date(item.created_at).toLocaleString()}</td>
                                        <td className="p-3">{new Date(item.updated_at).toLocaleString()}</td>
                                        <td className="p-3 flex justify-end gap-2">
                                            <Button variant="outline" size="icon" onClick={() => openDialog(item)}>
                                                <Edit className="h-4 w-4" />
                                            </Button>
                                            <AlertDialog open={isAlertOpen && selectedAirline?.id === item.id} onOpenChange={(open) => !open && setSelectedAirline(null)}>
                                                <AlertDialogTrigger asChild>
                                                    <Button variant="destructive" size="icon" onClick={() => openAlertDialog(item)}>
                                                        <Trash className="h-4 w-4" />
                                                    </Button>
                                                </AlertDialogTrigger>
                                                <AlertDialogContent>
                                                    <AlertDialogHeader>
                                                        <AlertDialogTitle>Bạn có chắc chắn muốn xóa?</AlertDialogTitle>
                                                        <AlertDialogDescription>
                                                            Hành động này không thể được hoàn tác. Dữ liệu hãng hàng không
                                                            <span className="font-bold"> {selectedAirline?.airlines_name} ({selectedAirline?.carrier}) </span>
                                                            sẽ bị xóa vĩnh viễn.
                                                        </AlertDialogDescription>
                                                    </AlertDialogHeader>
                                                    <AlertDialogFooter>
                                                        <AlertDialogCancel onClick={() => setIsAlertOpen(false)}>Hủy</AlertDialogCancel>
                                                        <AlertDialogAction onClick={handleDelete}>Xóa</AlertDialogAction>
                                                    </AlertDialogFooter>
                                                </AlertDialogContent>
                                            </AlertDialog>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div className="flex items-center justify-between space-x-2 py-4">
                    <div className="flex items-center space-x-2">
                        <p className="text-sm font-medium">Số hàng mỗi trang</p>
                        <Select
                            value={`${itemsPerPage}`}
                            onValueChange={handleItemsPerPageChange}
                        >
                            <SelectTrigger className="h-8 w-[80px]">
                                <SelectValue placeholder={itemsPerPage} />
                            </SelectTrigger>
                            <SelectContent side="top">
                                {[10, 20, 50, 100].map((pageSize) => (
                                    <SelectItem key={pageSize} value={`${pageSize}`}>
                                        {pageSize}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="flex items-center space-x-2">
                        <Button
                            variant="outline"
                            className="hidden h-8 w-8 p-0 lg:flex"
                            onClick={() => goToPage(1)}
                            disabled={currentPage === 1}
                        >
                            <span className="sr-only">Go to first page</span>
                            <ChevronsLeft className="h-4 w-4" />
                        </Button>
                        <Button
                            variant="outline"
                            className="h-8 w-8 p-0"
                            onClick={() => goToPage(currentPage - 1)}
                            disabled={currentPage === 1}
                        >
                            <span className="sr-only">Go to previous page</span>
                            <ChevronLeft className="h-4 w-4" />
                        </Button>
                        <div className="flex w-[100px] items-center justify-center text-sm font-medium">
                            Trang {currentPage} / {totalPages}
                        </div>
                        <Button
                            variant="outline"
                            className="h-8 w-8 p-0"
                            onClick={() => goToPage(currentPage + 1)}
                            disabled={currentPage === totalPages}
                        >
                            <span className="sr-only">Go to next page</span>
                            <ChevronRight className="h-4 w-4" />
                        </Button>
                        <Button
                            variant="outline"
                            className="hidden h-8 w-8 p-0 lg:flex"
                            onClick={() => goToPage(totalPages)}
                            disabled={currentPage === totalPages}
                        >
                            <span className="sr-only">Go to last page</span>
                            <ChevronsRight className="h-4 w-4" />
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Airline;
