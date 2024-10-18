import styles from './styles.module.css';

export const ErrorPage = () => {
    return (
        <main className={styles.page}>
            <h1>Ошибочка!</h1>
            <h3 className={styles.subheader}>
                Попробуй перезагрузить страницу или вернуться на главную
            </h3>
        </main>
    );
};