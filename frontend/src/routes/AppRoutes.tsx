import {

    Routes,

    Route,

    Navigate,

} from "react-router-dom";

import DashboardLayout from "../layouts/DashboardLayout";

import Dashboard from "../pages/Dashboard/Dashboard";

import Products from "../pages/Products/Products";

import Scout from "../pages/Scout/Scout";

import Analytics from "../pages/Analytics/Analytics";

import Settings from "../pages/Settings/Settings";

export default function AppRoutes() {

    return (

        <DashboardLayout>

            <Routes>

                <Route

                    path="/"

                    element={<Navigate to="/dashboard" replace />}

                />

                <Route

                    path="/dashboard"

                    element={<Dashboard />}

                />

                <Route

                    path="/products"

                    element={<Products />}

                />

                <Route

                    path="/scout"

                    element={<Scout />}

                />

                <Route

                    path="/analytics"

                    element={<Analytics />}

                />

                <Route

                    path="/settings"

                    element={<Settings />}

                />

            </Routes>

        </DashboardLayout>

    );

}