import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router";
import Layout from "@/layout";
import Index from "@/pages/Index";
import NotFound from "@/components/NotFound";
import DimAircraft from "@/pages/temp/Aircraft";
import DimAirline from "@/pages/temp/Airline";
import DimAirport from "@/pages/temp/Airport";
import DimCountry from "@/pages/temp/Country";
import DimSectorRoute from "@/pages/temp/SectorRoute";
import Aircraft from "@/pages/manager/Aircraft";
import Airline from "@/pages/manager/Airline";
import Airport from "@/pages/manager/Airport";
import Country from "@/pages/manager/Country";
import SectorRoute from "@/pages/manager/SectorRoute";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout><Index /></Layout>} />
        <Route path="/temp/aircraft" element={<Layout><DimAircraft /></Layout>} />
        <Route path="/temp/airline" element={<Layout><DimAirline /></Layout>} />
        <Route path="/temp/airport" element={<Layout><DimAirport /></Layout>} />
        <Route path="/temp/country" element={<Layout><DimCountry /></Layout>} />
        <Route path="/temp/sector-route" element={<Layout><DimSectorRoute /></Layout>} />
        <Route path="/manager/aircraft" element={<Layout><Aircraft /></Layout>} />
        <Route path="/manager/airline" element={<Layout><Airline /></Layout>} />
        <Route path="/manager/airport" element={<Layout><Airport /></Layout>} />
        <Route path="/manager/country" element={<Layout><Country /></Layout>} />
        <Route path="/manager/sector-route" element={<Layout><SectorRoute /></Layout>} />
        {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  </QueryClientProvider>
);

export default App;