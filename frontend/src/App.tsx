import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router";
import Layout from "@/layout";
import Index from "@/pages/Index";
import NotFound from "@/components/NotFound";
import Aircraft from "@/pages/Aircraft";
import Airline from "@/pages/Airline";
import Airport from "@/pages/Airport";
import Country from "@/pages/Country";
import SectorRoute from "@/pages/SectorRoute";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout><Index /></Layout>} />
        <Route path="/aircraft" element={<Layout><Aircraft /></Layout>} />
        <Route path="/airline" element={<Layout><Airline /></Layout>} />
        <Route path="/airport" element={<Layout><Airport /></Layout>} />
        <Route path="/country" element={<Layout><Country /></Layout>} />
        <Route path="/sector-route" element={<Layout><SectorRoute /></Layout>} />
        {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  </QueryClientProvider>
);

export default App;