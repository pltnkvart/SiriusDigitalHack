import { useCallback, useState } from "react";
import { PageLayout } from "../../components/PageLayout/PageLayout";
import { Button, Text, Tabs, TabsItemProps, useToaster } from "@gravity-ui/uikit";
import styles from './styles.module.css';
import * as XLSX from 'xlsx';
import { useNavigate } from "react-router-dom";

interface ExcelData {
    [key: string]: string | number | boolean;
}

export const InputFilePage = () => {
    const { add } = useToaster();
    const navigate = useNavigate();
    const [excelFile, setExcelFile] = useState<ArrayBuffer | null>(null);
    const [excelSheetsData, setExcelSheetsData] = useState<Record<string, ExcelData[]> | null>(null);
    const [tabSheets, setTabSheets] = useState<TabsItemProps[]>([]);
    const [activeSheet, setActiveSheet] = useState<string>();

    const onSelectTab = useCallback((tabId: string) => {
        const findSheet = tabSheets.find((tab) => tab.id === tabId);
        if (findSheet) setActiveSheet(findSheet.id);
    }, [tabSheets]);

    const handleFileRead = (e: React.ChangeEvent<HTMLInputElement>) => {
        const fileTypes = ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/csv'];
        const selectedFile = e.target.files?.[0];
        if (selectedFile && fileTypes.includes(selectedFile.type)) {
            const reader = new FileReader();
            reader.readAsArrayBuffer(selectedFile);
            reader.onload = (e) => {
                setExcelFile(e.target?.result as ArrayBuffer);
            };
        }
    };

    const handleFileSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (excelFile) {
            const workbook = XLSX.read(excelFile, { type: 'buffer' });
            const sheetsData: Record<string, ExcelData[]> = {};
            workbook.SheetNames.forEach((sheetName) => {
                const worksheet = workbook.Sheets[sheetName];
                const data = XLSX.utils.sheet_to_json(worksheet) as ExcelData[];
                sheetsData[sheetName] = data;
            });
            const tabList: TabsItemProps[] = workbook.SheetNames.map((sheetName) => ({
                id: sheetName,
                title: sheetName,
            }));
            setTabSheets(tabList);
            setActiveSheet(tabList[0].id);
            setExcelSheetsData(sheetsData);
            add({
                name: 'success',
                theme: 'success',
                title: 'Файл загружен',
            });
        }
    };

    const handleAnalyzeButtonClick = () => {
        const id = 1; // TODO
        navigate(`/analyze/${id}`)
    }

    return (
        <PageLayout>
            <Text variant="header-2" color="primary">Загрузка файла</Text>
            {!excelSheetsData ? <form onSubmit={handleFileSubmit}>
                <input type="file" className="form-control" required onChange={handleFileRead} />
                <Button
                    type="submit"
                    view="action"
                    size="m"
                    disabled={!excelFile && !excelSheetsData}
                >
                    Загрузить
                </Button>
            </form> : <Button
                type="submit"
                view="action"
                size="m"
                onClick={handleAnalyzeButtonClick}
                className={styles.analyze}
            >
                АНАЛИЗИРОВАТЬ!
            </Button>}
            {tabSheets && (
                <Tabs
                    activeTab={activeSheet}
                    items={tabSheets}
                    onSelectTab={onSelectTab}
                />
            )}
            <div className={styles.viewer}>
                {activeSheet && excelSheetsData && excelSheetsData ? (
                    <div className="sheet-section">
                        <div className="table-responsive">
                            <table className={styles.styled_table}>
                                <thead>
                                    <tr>
                                        {excelSheetsData[activeSheet].length > 0 && Object.keys(excelSheetsData[activeSheet][0]).map((key) => (
                                            <th key={key}>{key}</th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody>
                                    {excelSheetsData[activeSheet].map((individualExcelData, index) => (
                                        <tr key={index}>
                                            {Object.keys(individualExcelData).map((key) => (
                                                <td key={key}>{individualExcelData[key]}</td>
                                            ))}
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                ) : (
                    <div>Нет файла</div>
                )}
            </div>
        </PageLayout>
    );
}
