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
import Sales from "../pages/Sales/Sales";
import Inspector from "../pages/Inspector/Inspector";
import Settings from "../pages/Settings/Settings";
import Accounts from "../pages/Accounts/Accounts";
import Admin from "../pages/Admin/Admin";
import Funnel from "../pages/Funnel/Funnel";
import Discovery from "../pages/Discovery/Discovery";
import ContentStrategyPage from "../pages/ContentStrategy/ContentStrategy";
import FollowUps from "../pages/FollowUps/FollowUps";
import Channels from "../pages/Channels/Channels";
import Seasonal from "../pages/Seasonal/Seasonal";
import Automation from "../pages/Automation/Automation";
import DivulgationGroups from "../pages/DivulgationGroups/DivulgationGroups";
import FirstSalePlan from "../pages/FirstSalePlan/FirstSalePlan";
import AuditLog from "../pages/AuditLog/AuditLog";
import Vocabulary from "../pages/Vocabulary/Vocabulary";
import WhatsApp from "../pages/WhatsApp/WhatsApp";
import AIAgent from "../pages/AIAgent/AIAgent";

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
                                    path="/sales"
                                    element={<Sales />}
                                />

                                <Route
                                    path="/inspector"
                                    element={<Inspector />}
                                />

                                <Route
                                    path="/settings"
                                    element={<Settings />}
                                />

                                <Route
                                    path="/accounts"
                                    element={<Accounts />}
                                />

                                <Route
                                    path="/funnel"
                                    element={<Funnel />}
                                />

                                <Route
                                    path="/discovery"
                                    element={<Discovery />}
                                />

                                <Route
                                    path="/content-strategy"
                                    element={<ContentStrategyPage />}
                                />

                                <Route
                                    path="/follow-ups"
                                    element={<FollowUps />}
                                />

                                <Route
                                    path="/channels"
                                    element={<Channels />}
                                />

                                <Route
                                    path="/seasonal"
                                    element={<Seasonal />}
                                />

                                <Route
                                    path="/automation"
                                    element={<Automation />}
                                />

                                <Route
                                    path="/divulgation-groups"
                                    element={<DivulgationGroups />}
                                />
                                <Route
                                    path="/first-sale-plan"
                                    element={<FirstSalePlan />}
                                />

                                <Route
                                    path="/audit-log"
                                    element={<AuditLog />}
                                />

                                <Route
                                    path="/vocabulary"
                                    element={<Vocabulary />}
                                />

                                <Route
                                    path="/whatsapp"
                                    element={<WhatsApp />}
                                />

                                <Route
                                    path="/ai-agent"
                                    element={<AIAgent />}
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
