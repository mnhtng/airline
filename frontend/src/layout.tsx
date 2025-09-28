import type { ReactNode } from "react";
import { Link, useLocation } from "react-router";
import { Button } from "@/components/ui/button";
import { Plane, Route, Home } from "lucide-react";
import { Toaster } from 'sonner';

interface LayoutProps {
    children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
    const location = useLocation();

    const navItems = [
        { path: "/", label: "Trang chủ", icon: Home, color: "text-red-300" },
        { path: "/aircraft", label: "Máy bay", icon: Plane, color: "text-blue-300" },
        { path: "/airway", label: "Đường bay", icon: Route, color: "text-green-400" },
    ];

    return (
        <div className="min-h-screen bg-background">
            <header className="sky-gradient border-b border-border/20 shadow-lg sticky top-0 z-100 md:static">
                <div className="container mx-auto px-4 py-4">
                    <div className="flex items-center justify-between">
                        <Link to="/" className="flex items-center space-x-3">
                            <Plane className="h-8 w-8 text-primary-foreground" />
                            <h1 className="text-2xl font-bold text-primary-foreground hidden sm:inline">
                                Vina Entry Hub
                            </h1>
                        </Link>

                        <nav className="flex space-x-2">
                            {navItems.map(({ path, label, icon: Icon, color }) => (
                                <Button
                                    key={path}
                                    variant={location.pathname === path ? "secondary" : "ghost"}
                                    size="sm"
                                    asChild
                                    className={location.pathname === path ?
                                        "bg-foreground/50 text-primary-foreground hover:bg-foreground/70" :
                                        "text-foreground/80 hover:text-primary-foreground hover:bg-foreground/50"
                                    }
                                >
                                    <Link to={path} className="flex items-center space-x-0 sm:space-x-2">
                                        <Icon className={`h-4 w-4 ${location.pathname === path && color}`} />
                                        <span className="hidden sm:inline">{label}</span>
                                    </Link>
                                </Button>
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