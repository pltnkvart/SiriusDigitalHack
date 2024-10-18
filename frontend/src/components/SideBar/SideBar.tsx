import React, { useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { AsideHeader, MenuItem } from '@gravity-ui/navigation';
import { Shapes4 } from '@gravity-ui/icons';
import { MENU_ITEMS, SERVICE_NAME } from '../../types/constants';

export interface ISideBarProps {
    children: React.ReactNode;
}

export const SideBar = ({ children }: ISideBarProps) => {
    const navigate = useNavigate();
    const location = useLocation();
    const [compact, setCompact] = useState(false);

    const renderContent = React.useCallback(() => children, [children]);

    const menuItems: MenuItem[] = useMemo(() => {
        return MENU_ITEMS.map((menuItem) => ({
            ...menuItem,
            current: location.pathname.startsWith(menuItem.path),
            onItemClick: () => {
                navigate(menuItem.path);
            },
        }));
    }, [navigate, location.pathname]);

    return (
        <AsideHeader
            compact={compact}
            menuItems={menuItems}
            onChangeCompact={setCompact}
            headerDecoration
            logo={{
                icon: Shapes4,
                text: SERVICE_NAME,
            }}
            renderContent={renderContent}
            multipleTooltip
        />
    );
};