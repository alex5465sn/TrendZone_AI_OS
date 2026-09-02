import {
    Routes,
    Route,
    Navigate,
} from "react-router-dom";

import DashboardLayout from "../layouts/DashboardLayout";
import Login from "../pages/Login/Login";
import Register from "../pages/Register/Register";
import Dashboard from "../pages/Dashboard/Dashboard";
import Products from "../pages/Products/Products";
import Scout from "../pages/Scout/Scout";
import Analytics from "../pages/Analytics/Analytics";
import Opportunities from "../pages/Opportunities/Opportunities";
import Prospects from "../pages/Prospects/Prospects";
import Settings from "../pages/Settings/Settings";
import Admin from "../pages/Admin/Admin";

import { isAuthenticated, isAdmin } from "../services/authService";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
    if (!isAuthenticated()) {
        return <Navigate to="/login" replace />;
    }
    return <>{children}</>;
}

function AdminRoute({ children }: { children: React.ReactNode }) {
    if (!isAuthenticated()) {
        return <Navigate to="/login" replace />;
    }
    if (!isAdmin()) {
        return <Navigate to="/dashboard" replace />;
    }
    return <>{children}</>;
}

export default function AppRoutes() {

    return (

        <Routes>

            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            <Route
                path="/*"
                element={
                    <ProtectedRoute>
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
                                    path="/opportunities"
                                    element={<Opportunities />}
                                />

                                <Route
                                    path="/prospects"
                                    element={<Prospects />}
                                />

                                <Route
                                    path="/settings"
                                    element={<Settings />}
                                />

                            </Routes>
                        </DashboardLayout>
                    </ProtectedRoute>
                }
            />

            <Route
                path="/admin"
                element={
                    <AdminRoute>
                        <DashboardLayout>
                            <Admin />
                        </DashboardLayout>
                    </AdminRoute>
                }
            />

        </Routes>

    );

}
