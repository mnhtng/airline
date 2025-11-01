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

interface Country {
    id: number;
    country: string;
    region: string;
    region_vnm: string;
    two_letter_code: string;
    three_letter_code: string;
    created_at: string;
    updated_at: string;
}

const Country = () => {
    const [data, setData] = useState<Country[]>([])
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<string | null>(null)
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [isAlertOpen, setIsAlertOpen] = useState(false);
    const [selectedCountry, setSelectedCountry] = useState<Country | null>(null);
    const [formData, setFormData] = useState({ country: '', region: '', region_vnm: '', two_letter_code: '', three_letter_code: '' });
    const [formError, setFormError] = useState<string | null>(null);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage, setItemsPerPage] = useState(10);
    const [searchTerm, setSearchTerm] = useState("");

    async function getCountries(search: string = "") {
        setLoading(true)
        try {
            const url = search
                ? `${import.meta.env.VITE_API_URL}/countries/search/?q=${search}`
                : `${import.meta.env.VITE_API_URL}/countries/`;
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
            getCountries(searchTerm);
        }, 500); // 500ms debounce delay

        return () => clearTimeout(debounceTimer);
    }, [searchTerm]);

    const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { id, value } = e.target;
        setFormData(prev => ({ ...prev, [id]: value }));
    };

    const validateForm = () => {
        if (!formData.country.trim()) {
            setFormError('Tên quốc gia không được để trống.');
            return false;
        }
        if (!formData.two_letter_code.trim()) {
            setFormError('Mã 2 ký tự không được để trống.');
            return false;
        }
        if (formData.two_letter_code.trim().length !== 2) {
            setFormError('Mã 2 ký tự phải có đúng 2 ký tự.');
            return false;
        }
        if (!formData.three_letter_code.trim()) {
            setFormError('Mã 3 ký tự không được để trống.');
            return false;
        }
        if (formData.three_letter_code.trim().length !== 3) {
            setFormError('Mã 3 ký tự phải có đúng 3 ký tự.');
            return false;
        }
        setFormError(null);
        return true;
    };

    const handleCreateOrUpdate = async () => {
        if (!validateForm()) return;

        setIsSubmitting(true);
        const method = selectedCountry ? "PUT" : "POST";
        const url = selectedCountry
            ? `${import.meta.env.VITE_API_URL}/countries/${selectedCountry.id}`
            : `${import.meta.env.VITE_API_URL}/countries/`;

        const body = {
            country: formData.country.trim(),
            region: formData.region.trim(),
            region_vnm: formData.region_vnm.trim(),
            two_letter_code: formData.two_letter_code.trim().toUpperCase(),
            three_letter_code: formData.three_letter_code.trim().toUpperCase(),
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

            toast.success(`Đã ${selectedCountry ? 'cập nhật' : 'tạo mới'} quốc gia thành công!`);
            setIsDialogOpen(false);
            getCountries();
        } catch (error: any) {
            toast.error(error.message || `Không thể ${selectedCountry ? 'cập nhật' : 'tạo mới'} quốc gia.`);
        } finally {
            setIsSubmitting(false);
        }
    };


    const handleDelete = async () => {
        if (!selectedCountry) return;

        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/countries/${selectedCountry.id}`, {
                method: "DELETE"
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Có lỗi xảy ra");
            }

            toast.success("Đã xóa quốc gia thành công!");
            setIsAlertOpen(false);
            getCountries();
        } catch (error: any) {
            toast.error(error.message || "Không thể xóa quốc gia.");
        }
    };


    const openDialog = (country: Country | null) => {
        setSelectedCountry(country);
        setFormData(country ? { country: country.country, region: country.region, region_vnm: country.region_vnm, two_letter_code: country.two_letter_code, three_letter_code: country.three_letter_code } : { country: '', region: '', region_vnm: '', two_letter_code: '', three_letter_code: '' });
        setFormError(null);
        setIsDialogOpen(true);
    };

    const openAlertDialog = (country: Country) => {
        setSelectedCountry(country);
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
                    <h1 className="text-2xl font-bold">Quản Lý Quốc Gia</h1>
                    <div className="flex items-center gap-2">
                        <div className="relative">
                            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                type="search"
                                placeholder="Tìm kiếm quốc gia..."
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
                            <DialogContent className="sm:max-w-[525px]">
                                <DialogHeader>
                                    <DialogTitle>{selectedCountry ? "Chỉnh Sửa Quốc Gia" : "Thêm Quốc Gia Mới"}</DialogTitle>
                                    <DialogDescription>
                                        {selectedCountry ? "Cập nhật thông tin quốc gia." : "Điền thông tin để tạo quốc gia mới."}
                                    </DialogDescription>
                                </DialogHeader>
                                <div className="grid gap-4 py-4">
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="country" className="text-right">Tên Quốc Gia</Label>
                                        <Input id="country" value={formData.country} onChange={handleFormChange} className="col-span-3" />
                                    </div>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="region" className="text-right">Khu Vực (QT)</Label>
                                        <Input id="region" value={formData.region} onChange={handleFormChange} className="col-span-3" />
                                    </div>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="region_vnm" className="text-right">Khu Vực (VN)</Label>
                                        <Input id="region_vnm" value={formData.region_vnm} onChange={handleFormChange} className="col-span-3" />
                                    </div>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="two_letter_code" className="text-right">Mã 2 Ký Tự</Label>
                                        <Input id="two_letter_code" value={formData.two_letter_code} onChange={handleFormChange} className="col-span-3" />
                                    </div>
                                    <div className="grid grid-cols-4 items-center gap-4">
                                        <Label htmlFor="three_letter_code" className="text-right">Mã 3 Ký Tự</Label>
                                        <Input id="three_letter_code" value={formData.three_letter_code} onChange={handleFormChange} className="col-span-3" />
                                    </div>
                                    {formError && <p className="col-span-4 text-red-500 text-sm text-center">{formError}</p>}
                                </div>
                                <DialogFooter>
                                    <DialogClose asChild><Button type="button" variant="secondary">Hủy</Button></DialogClose>
                                    <Button onClick={handleCreateOrUpdate} disabled={isSubmitting}>
                                        {isSubmitting && <Loader className="mr-2 h-4 w-4 animate-spin" />}
                                        {selectedCountry ? "Lưu thay đổi" : "Tạo"}
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
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Quốc Gia</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Khu Vực (QT)</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Khu Vực (VN)</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Mã 2 Ký Tự</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Mã 3 Ký Tự</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Ngày Tạo</th>
                                    <th className="text-left text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Ngày Cập Nhật</th>
                                    <th className="text-right text-xs p-3 font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Hành Động</th>
                                </tr>
                            </thead>
                            <tbody>
                                {loading ? (
                                    <tr><td colSpan={7} className="py-6 text-center"><Loading /></td></tr>
                                ) : error ? (
                                    <tr><td colSpan={7}><ErrorBanner title={error} description="Có lỗi xảy ra khi tải dữ liệu. Vui lòng thử lại." retry={() => getCountries(searchTerm)} /></td></tr>
                                ) : data.length === 0 ? (
                                    <tr><td colSpan={7} className="p-3 text-center text-slate-500">Không có dữ liệu</td></tr>
                                ) : paginatedData.map((item, index) => (
                                    <tr key={item.id} className={`border-b border-slate-200/40 dark:border-slate-700/40 hover:bg-sky-200/35 dark:hover:bg-sky-800/30 transition-all duration-200 group ${index % 2 === 0 ? "bg-white/40 dark:bg-slate-900/40" : "bg-slate-50/20 dark:bg-slate-800/20"}`}>
                                        <td className="p-3 font-medium">{item.country}</td>
                                        <td className="p-3">{item.region}</td>
                                        <td className="p-3">{item.region_vnm}</td>
                                        <td className="p-3">{item.two_letter_code}</td>
                                        <td className="p-3">{item.three_letter_code}</td>
                                        <td className="p-3">{new Date(item.created_at).toLocaleString()}</td>
                                        <td className="p-3">{new Date(item.updated_at).toLocaleString()}</td>
                                        <td className="p-3 flex justify-end gap-2">
                                            <Button variant="outline" size="icon" onClick={() => openDialog(item)}><Edit className="h-4 w-4" /></Button>
                                            <AlertDialog open={isAlertOpen && selectedCountry?.id === item.id} onOpenChange={(open) => !open && setSelectedCountry(null)}>
                                                <AlertDialogTrigger asChild>
                                                    <Button variant="destructive" size="icon" onClick={() => openAlertDialog(item)}>
                                                        <Trash className="h-4 w-4" />
                                                    </Button>
                                                </AlertDialogTrigger>
                                                <AlertDialogContent>
                                                    <AlertDialogHeader>
                                                        <AlertDialogTitle>Bạn có chắc chắn muốn xóa?</AlertDialogTitle>
                                                        <AlertDialogDescription>
                                                            Hành động này không thể được hoàn tác. Dữ liệu quốc gia
                                                            <span className="font-bold"> {selectedCountry?.country} </span>
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

export default Country;
