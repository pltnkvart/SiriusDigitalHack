import styles from './styles.module.css';
import { Loader } from '@gravity-ui/uikit';

interface IPageLayoutProps {
    children: React.ReactNode;
    isLoading?: boolean;
}

export const PageLayout = ({ children, isLoading }: IPageLayoutProps) => {
    return (
        <main className={styles.page}>
            {isLoading ? <Loader /> : children}
        </main>
    )
}