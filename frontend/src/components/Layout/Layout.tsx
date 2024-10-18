import { SideBar } from "../SideBar/SideBar";

interface ILayoutProps {
    children?: React.ReactNode[] | React.ReactNode;
}

export const Layout = ({ children }: ILayoutProps) => {
    return <SideBar>{children}</SideBar>;
};