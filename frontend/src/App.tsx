import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router";
import Layout from "@/layout";
import Index from "@/pages/Index";
import NotFound from "@/components/NotFound";
import Aircraft from "@/pages/Aircraft";
import Airway from "@/pages/Airway";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout><Index /></Layout>} />
        <Route path="/aircraft" element={<Layout><Aircraft /></Layout>} />
        <Route path="/airway" element={<Layout><Airway /></Layout>} />
        {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  </QueryClientProvider>
);

export default App;