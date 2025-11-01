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
} from "lucide-react"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { Search } from "lucide-react"
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

interface Aircraft {
    actype: string
    seat: number
    created_at: string
    updated_at: string
}

const Aircraft = () => {
    const [data, setData] = useState<Aircraft[]>([])
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<string | null>(null)
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [isAlertOpen, setIsAlertOpen] = useState(false);
    const [selectedAircraft, setSelectedAircraft] = useState<Aircraft | null>(null);
    const [formData, setFormData] = useState({ actype: '', seat: '' });
    const [formError, setFormError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(10);
    const [searchTerm, setSearchTerm] = useState("");


    async function getAircrafts(search: string = "") {
        setLoading(true)
        try {
            const url = search
                ? `${import.meta.env.VITE_API_URL}/actype-seats/search/?q=${search}`
                : `${import.meta.env.VITE_API_URL}/actype-seats/`;
            const response = await fetch(url)
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
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
        const debounceTimer = setTimeout(() => {
            getAircrafts(searchTerm);
        }, 500); // 500ms debounce delay

        return () => clearTimeout(debounceTimer);
    }, [searchTerm]);

    const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { id, value } = e.target;
        setFormData(prev => ({ ...prev, [id]: value }));
    };

    const validateForm = () => {
        if (!formData.actype.trim()) {
            setFormError('Mã máy bay không được để trống.');
            return false;
        }
        if (!formData.seat || parseInt(formData.seat) <= 0) {
            setFormError('Số ghế phải là một số dương.');
            return false;
        }
        setFormError(null);
        return true;
    };

    const handleCreateOrUpdate = async () => {
        if (!validateForm()) return;

        setIsSubmitting(true);
        const method = selectedAircraft ? "PUT" : "POST";
        const url = selectedAircraft
            ? `${import.meta.env.VITE_API_URL}/actype-seats/${selectedAircraft.actype}`
            : `${import.meta.env.VITE_API_URL}/actype-seats/`;

        const body = {
            actype: formData.actype.trim().toUpperCase(),
            seat: parseInt(formData.seat)
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

            toast.success(`Đã ${selectedAircraft ? 'cập nhật' : 'tạo mới'} máy bay thành công!`);
            setIsDialogOpen(false);
            getAircrafts(); // Refresh data
        } catch (error: any) {
            toast.error(error.message || `Không thể ${selectedAircraft ? 'cập nhật' : 'tạo mới'} máy bay.`);
        } finally {
            setIsSubmitting(false);
        }
    };


    const handleDelete = async () => {
        if (!selectedAircraft) return;

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/actype-seats/${selectedAircraft.actype}`, {
                method: "DELETE"
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Có lỗi xảy ra");
            }

            toast.success("Đã xóa máy bay thành công!");
            setIsAlertOpen(false);
            getAircrafts(); // Refresh data
        } catch (error: any) {
            toast.error(error.message || "Không thể xóa máy bay.");
        }
    };


    const openDialog = (aircraft: Aircraft | null) => {
        setSelectedAircraft(aircraft);
        setFormData(aircraft ? { actype: aircraft.actype, seat: aircraft.seat.toString() } : { actype: '', seat: '' });
        setFormError(null);
        setIsDialogOpen(true);
    };

    const openAlertDialog = (aircraft: Aircraft) => {
        setSelectedAircraft(aircraft);
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
                <div className="mb-8 flex justify-between items-center">
                    <h1 className="text-2xl font-bold">Quản Lý Máy Bay</h1>
                    <div className="flex items-center gap-2">
                        <div className="relative">
                            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                type="search"
                                placeholder="Tìm kiếm máy bay..."
                                className="pl-8 sm:w-[300px]"
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
                                    <DialogTitle>{selectedAircraft ? "Chỉnh Sửa Máy Bay" : "Thêm Máy Bay Mới"}</DialogTitle>
                                    <DialogDescription>
                                        {selectedAircraft ? "Cập nhật thông tin máy bay." : "Điền thông tin để tạo máy bay mới."}
                                    </DialogDescription>
                                </DialogHeader>
                                <div className="grid gap-4 py-4">
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="actype" className="text-right">
                                            Mã Máy Bay
                                        </Label>
                                        <Input id="actype" value={formData.actype} onChange={handleFormChange} className="col-span-3" disabled={!!selectedAircraft} />
                                    </div>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="seat" className="text-right">
                                            Số Ghế
                                        </Label>
                                        <Input id="seat" type="number" min="1" value={formData.seat} onChange={handleFormChange} className="col-span-3" />
                                    </div>
                                    {formError && <p className="col-span-4 text-red-500 text-sm text-center">{formError}</p>}
                                </div>
                                <DialogFooter>
                                    <DialogClose asChild>
                                        <Button type="button" variant="secondary">Hủy</Button>
                                    </DialogClose>
                                    <Button onClick={handleCreateOrUpdate} disabled={isSubmitting}>
                                        {isSubmitting && <Loader className="mr-2 h-4 w-4 animate-spin" />}
                                        {selectedAircraft ? "Lưu thay đổi" : "Tạo"}
                                    </Button>
                                </DialogFooter>
                            </DialogContent>
                        </Dialog>
                    </div>
                </div>

                <div className="bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm rounded-2xl border border-slate-400 shadow-xl shadow-slate-200/20 dark:shadow-slate-900/20 overflow-hidden">
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead>
                                <tr className="border-b border-slate-400 bg-slate-300/30 dark:bg-slate-800/50">
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Mã Máy Bay</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Số Ghế</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Ngày Tạo</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Ngày Cập Nhật</th>
                                    <th className="text-right text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Hành Động</th>
                                </tr>
                            </thead>
                            <tbody>
                                {loading ? (
                                    <tr><td colSpan={5} className="py-6 text-center"><Loading /></td></tr>
                                ) : error ? (
                                    <tr><td colSpan={5}><ErrorBanner title={error} description="Có lỗi xảy ra khi tải dữ liệu. Vui lòng thử lại." retry={() => getAircrafts(searchTerm)} /></td></tr>
                                ) : data.length === 0 ? (
                                    <tr><td colSpan={5} className="p-3 text-center text-slate-500">Không có dữ liệu</td></tr>
                                ) : paginatedData.map((item, index) => (
                                    <tr key={item.actype} className={`border-b border-slate-200/40 dark:border-slate-700/40 hover:bg-sky-200/35 dark:hover:bg-sky-800/30 transition-all duration-200 group ${index % 2 === 0 ? "bg-white/40 dark:bg-slate-900/40" : "bg-slate-50/20 dark:bg-slate-800/20"}`}>
                                        <td className="p-3 font-medium">{item.actype}</td>
                                        <td className="p-3">{item.seat}</td>
                                        <td className="p-3">{new Date(item.created_at).toLocaleString()}</td>
                                        <td className="p-3">{new Date(item.updated_at).toLocaleString()}</td>
                                        <td className="p-3 flex justify-end gap-2">
                                            <Button variant="outline" size="icon" onClick={() => openDialog(item)}>
                                                <Edit className="h-4 w-4" />
                                            </Button>
                                            <AlertDialog open={isAlertOpen && selectedAircraft?.actype === item.actype} onOpenChange={(open) => !open && setSelectedAircraft(null)}>
                                                <AlertDialogTrigger asChild>
                                                    <Button variant="destructive" size="icon" onClick={() => openAlertDialog(item)}>
                                                        <Trash className="h-4 w-4" />
                                                    </Button>
                                                </AlertDialogTrigger>
                                                <AlertDialogContent>
                                                    <AlertDialogHeader>
                                                        <AlertDialogTitle>Bạn có chắc chắn muốn xóa?</AlertDialogTitle>
                                                        <AlertDialogDescription>
                                                            Hành động này không thể được hoàn tác. Dữ liệu máy bay
                                                            <span className="font-bold"> {selectedAircraft?.actype} </span>
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

export default Aircraft;
