import type { ReactNode } from "react";
import { Link, useLocation } from "react-router";
import { Button } from "@/components/ui/button";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
    Plane, Route, Building2, Landmark, Globe2, ChevronDown, BookOpenCheck, Settings
} from "lucide-react";
import { Toaster } from 'sonner';
import { useState } from "react";

interface LayoutProps {
    children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
    const location = useLocation();
    const [hoveredDropdown, setHoveredDropdown] = useState<string | null>(null);
    const [clickedDropdown, setClickedDropdown] = useState<string | null>(null);

    // Handle hover logic
    const handleMouseEnter = (menuLabel: string) => {
        setHoveredDropdown(menuLabel);
    };

    const handleMouseLeave = () => {
        setHoveredDropdown(null);
    };

    // Handle click logic
    const handleClick = (menuLabel: string) => {
        setClickedDropdown(clickedDropdown === menuLabel ? null : menuLabel);
    };

    // Check if dropdown should be open (either hovered or clicked)
    const isDropdownOpen = (menuLabel: string) => {
        return hoveredDropdown === menuLabel || clickedDropdown === menuLabel;
    };

    const dropdownMenus = [
        {
            label: "Phiếu điền",
            icon: BookOpenCheck,
            items: [
                { path: "/aircraft", label: "Máy bay", icon: Plane, color: "text-blue-700" },
                { path: "/airport", label: "Sân bay", icon: Landmark, color: "text-orange-700" },
                { path: "/airline", label: "Hãng hàng không", icon: Building2, color: "text-purple-700" },
                { path: "/country", label: "Quốc gia", icon: Globe2, color: "text-cyan-700" },
                { path: "/sector-route", label: "Phân loại đường bay", icon: Route, color: "text-green-700" },
            ]
        },
        {
            label: "Quản lý",
            icon: Settings,
            items: [
                { path: "/", label: "Máy bay", icon: Plane, color: "text-blue-700" },
                { path: "/", label: "Sân bay", icon: Landmark, color: "text-orange-700" },
                { path: "/", label: "Hãng hàng không", icon: Building2, color: "text-purple-700" },
                { path: "/", label: "Quốc gia", icon: Globe2, color: "text-cyan-700" },
                { path: "/", label: "Phân loại đường bay", icon: Route, color: "text-green-700" },
            ]
        }
    ];

    return (
        <div className="min-h-screen bg-background">
            <header className="border-b border-border/20 shadow-lg sticky top-0 z-50" style={{
                background: 'linear-gradient(135deg, #ffc20f, #fff1c8 90%)',
            }}>
                <div className="container mx-auto px-4 py-3">
                    <div className="flex items-center justify-between">
                        {/* Logo */}
                        <Link to="/" className="flex items-center space-x-3 text-black hover:opacity-80 transition-opacity">
                            <img src="/app.png" alt="Logo" className="h-12 w-12 rounded-full" />
                            <h1 className="text-xl lg:text-2xl font-bold hidden md:inline">
                                Sun Phu Quoc Airways
                            </h1>
                        </Link>

                        <nav className="flex items-center space-x-1">
                            {dropdownMenus.map((menu) => (
                                <div
                                    key={menu.label}
                                    className="relative"
                                    onMouseEnter={() => handleMouseEnter(menu.label)}
                                    onMouseLeave={handleMouseLeave}
                                >
                                    <DropdownMenu
                                        open={isDropdownOpen(menu.label)}
                                        onOpenChange={(open) => {
                                            if (!open) {
                                                setHoveredDropdown(null);
                                                setClickedDropdown(null);
                                            }
                                        }}
                                    >
                                        <DropdownMenuTrigger asChild>
                                            <Button
                                                variant="ghost"
                                                size="sm"
                                                onClick={() => handleClick(menu.label)}
                                                className="flex items-center space-x-2 px-3 py-2 text-foreground/80 hover:text-primary-foreground hover:bg-foreground/30 hover:shadow-sm transition-all duration-200"
                                            >
                                                <menu.icon className="h-4 w-4" />
                                                <span className="text-sm font-medium">{menu.label}</span>
                                                <ChevronDown className={`h-3 w-3 transition-transform duration-200 ${isDropdownOpen(menu.label) ? 'rotate-180' : ''
                                                    }`} />
                                            </Button>
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent
                                            className="w-64"
                                            align="start"
                                            sideOffset={0}
                                        >
                                            {menu.items.map((item) => (
                                                <DropdownMenuItem key={item.path} asChild>
                                                    <Link
                                                        to={item.path}
                                                        onClick={() => {
                                                            setClickedDropdown(null);
                                                            setHoveredDropdown(null);
                                                        }}
                                                        className={`flex items-center space-x-3 px-3 py-2 cursor-pointer ${location.pathname === item.path ? "bg-muted/30" : ""
                                                            }`}
                                                    >
                                                        <item.icon className={`h-4 w-4 ${item.color}`} />
                                                        <span className="text-sm font-medium">{item.label}</span>
                                                    </Link>
                                                </DropdownMenuItem>
                                            ))}
                                        </DropdownMenuContent>
                                    </DropdownMenu>
                                </div>
                            ))}
                        </nav>
                    </div>
                </div>
            </header>

            <main className="container mx-auto px-4 py-8">
                {children}
            </main>

            <Toaster
                richColors
                position="top-center"
            />
        </div>
    );
};

export default Layout;