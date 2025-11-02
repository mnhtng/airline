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

interface SectorRoute {
    id: number;
    sector: string;
    area_lv1: string;
    dom_int: string;
    created_at: string;
    updated_at: string;
}

const SectorRoute = () => {
    const [data, setData] = useState<SectorRoute[]>([])
    const [exportData, setExportData] = useState<SectorRoute[]>([])
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<string | null>(null)
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [isAlertOpen, setIsAlertOpen] = useState(false);
    const [selectedSectorRoute, setSelectedSectorRoute] = useState<SectorRoute | null>(null);
    const [formData, setFormData] = useState({ sector: '', area_lv1: '', dom_int: '' });
    const [formError, setFormError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(10);
    const [searchTerm, setSearchTerm] = useState("");

    async function getSectorRoutes(search: string = "") {
        setLoading(true)
        try {
            const url = search
                ? `${import.meta.env.VITE_API_URL}/sector-route-doms/search/?q=${search}`
                : `${import.meta.env.VITE_API_URL}/sector-route-doms/`;
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
            getSectorRoutes(searchTerm);
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

        const filteredData = exportData.filter(SectorRoute => {
            const updateDate = SectorRoute.updated_at ? new Date(SectorRoute.updated_at) : new Date(SectorRoute.created_at);
            return updateDate >= start && updateDate <= end;
        })

        if (filteredData.length === 0) {
            toast.warning("Không có dữ liệu trong khoảng thời gian đã chọn!", {
                description: "Vui lòng chọn khoảng thời gian khác."
            })
            return
        }

        import("xlsx").then((XLSX) => {
            const excelData = filteredData.map((sectorRouteDom, index) => ({
                "STT": index + 1,
                "Mã Sector": sectorRouteDom.sector,
                "Vùng Cấp 1": sectorRouteDom.area_lv1,
                "Nội địa/Quốc tế": sectorRouteDom.dom_int,
                "Ngày Tạo": format(new Date(sectorRouteDom.created_at), "dd-MM-yyyy HH:mm:ss"),
                "Ngày Cập Nhật": sectorRouteDom.updated_at ? format(new Date(sectorRouteDom.updated_at), "dd-MM-yyyy HH:mm:ss") : "",
            }))

            const ws = XLSX.utils.json_to_sheet(excelData)
            const wb = XLSX.utils.book_new()
            XLSX.utils.book_append_sheet(wb, ws, "Sector Route DOMs")

            if ((end.getTime() - start.getTime()) <= 24 * 60 * 60 * 1000) {
                const fileName = `sector_route_doms_${format(start, "dd-MM-yyyy")}.xlsx`
                XLSX.writeFile(wb, fileName)
                return
            }

            const fileName = `sector_route_doms_${format(start, "dd-MM-yyyy")}_to_${format(end, "dd-MM-yyyy")}.xlsx`
            XLSX.writeFile(wb, fileName)
        })
    }

    const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { id, value } = e.target;
        setFormData(prev => ({ ...prev, [id]: value }));
    };

    const validateForm = () => {
        if (!formData.sector.trim()) {
            setFormError('Mã Sector không được để trống.');
            return false;
        }
        setFormError(null);
        return true;
    };

    const handleCreateOrUpdate = async () => {
        if (!validateForm()) return;

        setIsSubmitting(true);
        const method = selectedSectorRoute ? "PUT" : "POST";
        const url = selectedSectorRoute
            ? `${import.meta.env.VITE_API_URL}/sector-route-doms/${selectedSectorRoute.id}`
            : `${import.meta.env.VITE_API_URL}/sector-route-doms/`;

        const body = {
            sector: formData.sector.trim(),
            area_lv1: formData.area_lv1.trim(),
            dom_int: formData.dom_int.trim().toUpperCase(),
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

            toast.success(`Đã ${selectedSectorRoute ? 'cập nhật' : 'tạo mới'} tuyến bay thành công!`);
            setIsDialogOpen(false);
            getSectorRoutes();
        } catch (error: any) {
            toast.error(error.message || `Không thể ${selectedSectorRoute ? 'cập nhật' : 'tạo mới'} tuyến bay.`);
        } finally {
            setIsSubmitting(false);
        }
    };


    const handleDelete = async () => {
        if (!selectedSectorRoute) return;

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/sector-route-doms/${selectedSectorRoute.id}`, {
                method: "DELETE"
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Có lỗi xảy ra");
            }

            toast.success("Đã xóa tuyến bay thành công!");
            setIsAlertOpen(false);
            getSectorRoutes();
        } catch (error: any) {
            toast.error(error.message || "Không thể xóa tuyến bay.");
        }
    };


    const openDialog = (sectorRoute: SectorRoute | null) => {
        setSelectedSectorRoute(sectorRoute);
        setFormData(sectorRoute ? { sector: sectorRoute.sector, area_lv1: sectorRoute.area_lv1, dom_int: sectorRoute.dom_int } : { sector: '', area_lv1: '', dom_int: '' });
        setFormError(null);
        setIsDialogOpen(true);
    };

    const openAlertDialog = (sectorRoute: SectorRoute) => {
        setSelectedSectorRoute(sectorRoute);
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
                <h1 className="text-2xl font-bold text-center mb-10">Quản Lý Tuyến Bay</h1>

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
                                    placeholder="Tìm kiếm tuyến bay..."
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
                                        <DialogTitle>{selectedSectorRoute ? "Chỉnh Sửa Tuyến Bay" : "Thêm Tuyến Bay Mới"}</DialogTitle>
                                        <DialogDescription>
                                            {selectedSectorRoute ? "Cập nhật thông tin tuyến bay." : "Điền thông tin để tạo tuyến bay mới."}
                                        </DialogDescription>
                                    </DialogHeader>
                                    <div className="grid gap-4 py-4">
                                        <div className="grid grid-cols-4 items-center gap-4">
                                            <Label htmlFor="sector" className="text-right">Mã Sector</Label>
                                            <Input id="sector" value={formData.sector} onChange={handleFormChange} className="col-span-3" />
                                        </div>
                                        <div className="grid grid-cols-4 items-center gap-4">
                                            <Label htmlFor="area_lv1" className="text-right">Vùng Cấp 1</Label>
                                            <Input id="area_lv1" value={formData.area_lv1} onChange={handleFormChange} className="col-span-3" />
                                        </div>
                                        <div className="grid grid-cols-4 items-center gap-4">
                                            <Label htmlFor="dom_int" className="text-right">Nội địa/QT</Label>
                                            <Input id="dom_int" value={formData.dom_int} onChange={handleFormChange} className="col-span-3" />
                                        </div>
                                        {formError && <p className="col-span-4 text-red-500 text-sm text-center">{formError}</p>}
                                    </div>
                                    <DialogFooter>
                                        <DialogClose asChild><Button type="button" variant="secondary">Hủy</Button></DialogClose>
                                        <Button onClick={handleCreateOrUpdate} disabled={isSubmitting}>
                                            {isSubmitting && <Loader className="mr-2 h-4 w-4 animate-spin" />}
                                            {selectedSectorRoute ? "Lưu thay đổi" : "Tạo"}
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
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Mã Sector</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Vùng Cấp 1</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Nội địa/Quốc tế</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Ngày Tạo</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Ngày Cập Nhật</th>
                                    <th className="text-right text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Hành Động</th>
                                </tr>
                            </thead>
                            <tbody>
                                {loading ? (
                                    <tr><td colSpan={6} className="py-6 text-center"><Loading /></td></tr>
                                ) : error ? (
                                    <tr><td colSpan={6}><ErrorBanner title={error} description="Có lỗi xảy ra khi tải dữ liệu. Vui lòng thử lại." retry={() => getSectorRoutes(searchTerm)} /></td></tr>
                                ) : data.length === 0 ? (
                                    <tr><td colSpan={6} className="p-3 text-center text-slate-500">Không có dữ liệu</td></tr>
                                ) : paginatedData.map((item, index) => (
                                    <tr key={item.id} className={`border-b border-slate-200/40 dark:border-slate-700/40 hover:bg-sky-200/35 dark:hover:bg-sky-800/30 transition-all duration-200 group ${index % 2 === 0 ? "bg-white/40 dark:bg-slate-900/40" : "bg-slate-50/20 dark:bg-slate-800/20"}`}>
                                        <td className="p-3 font-medium">{item.sector}</td>
                                        <td className="p-3">{item.area_lv1}</td>
                                        <td className="p-3">{item.dom_int}</td>
                                        <td className="p-3">{new Date(item.created_at).toLocaleString()}</td>
                                        <td className="p-3">{new Date(item.updated_at).toLocaleString()}</td>
                                        <td className="p-3 flex justify-end gap-2">
                                            <Button variant="outline" size="icon" onClick={() => openDialog(item)}><Edit className="h-4 w-4" /></Button>
                                            <AlertDialog open={isAlertOpen && selectedSectorRoute?.id === item.id} onOpenChange={(open) => !open && setSelectedSectorRoute(null)}>
                                                <AlertDialogTrigger asChild>
                                                    <Button variant="destructive" size="icon" onClick={() => openAlertDialog(item)}>
                                                        <Trash className="h-4 w-4" />
                                                    </Button>
                                                </AlertDialogTrigger>
                                                <AlertDialogContent>
                                                    <AlertDialogHeader>
                                                        <AlertDialogTitle>Bạn có chắc chắn muốn xóa?</AlertDialogTitle>
                                                        <AlertDialogDescription>
                                                            Hành động này không thể được hoàn tác. Dữ liệu tuyến bay
                                                            <span className="font-bold"> {selectedSectorRoute?.sector} </span>
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

export default SectorRoute;
