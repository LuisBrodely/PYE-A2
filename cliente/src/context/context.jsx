import { createContext, useEffect, useState } from "react";
import axios from "axios";

export const Context = createContext();

export const ContextProvider = ({ children }) => {
    const [filePath, setFilePath] = useState('');
    const [tableHTML, setTableHTML] = useState(null);
    const [tableHTML2, setTableHTML2] = useState(null);
    const [columnaIndex, setColumnaIndex] = useState(0); // Estado para almacenar el índice de la columna seleccionada
    const [columnas, setColumnas] = useState([]); // Estado para almacenar las columnas de la tabla
    const [datosColumna, setDatosColumna] = useState([]); // Estado para almacenar los datos de la columna seleccionada
    const [chartImage, setChartImage] = useState('');
    const [chartImage2, setChartImage2] = useState('');
    const [chartImage3, setChartImage3] = useState('');
    const [chartImage4, setChartImage4] = useState('');
    const [chartImage5, setChartImage5] = useState('');

    const handleInputChange = (event) => {
        setFilePath(event.target.value);
    };
    const handleFileUpload = () => {
        const formData = new FormData();
        formData.append('file_path', filePath);

        axios.post('http://localhost:5000/upload', formData)
            .then(response => {
                // Manejar la respuesta del servidor
                setTableHTML(response.data.table_html);
            })
            .catch(error => {
                // Ocurrió un error al enviar la ruta del archivo
                console.error(error);
            });
    };
    const handleColumnaChange = (event) => {
        console.log(event.target.value)
        const columnData = {
            file_path: filePath,
            column_name: event.target.value
        };
        axios.post('http://localhost:5000/get_column_data', columnData)
            .then(response => {
                // Manejar la respuesta del servidor
                const imageSource = `data:image/png;base64, ${response.data.image1}`;
                const imageSource2 = `data:image/png;base64, ${response.data.image2}`;
                const imageSource3 = `data:image/png;base64, ${response.data.image3}`;
                const imageSource4 = `data:image/png;base64, ${response.data.image4}`;
                const imageSource5 = `data:image/png;base64, ${response.data.image5}`;
                setChartImage(imageSource);
                setChartImage2(imageSource2)
                setChartImage3(imageSource3)
                setChartImage4(imageSource4)
                setChartImage5(imageSource5)
            })
            .catch(error => {
                // Ocurrió un error al enviar la ruta del archivo
                console.error(error);
            });
        axios.post('http://localhost:5000/check_column_data', columnData)
            .then(response => {
                // Manejar la respuesta del servidor
                setTableHTML2(response.data.html_table);
                console.log(response)
            })
            .catch(error => {
                setTableHTML2(null)
                // Ocurrió un error al enviar la ruta del archivo
                console.error(error);
            });
    };
    useEffect(() => {
        obtenerColumnasTabla();
        console.log(datosColumna)
    }, [tableHTML]);

    const obtenerColumnasTabla = () => {
        if (tableHTML !== null) {
            const tabla = document.getElementsByClassName('dataframe');
            var tabla2 = tabla[0];
            console.log(tabla2)
            const encabezados = tabla2.querySelectorAll('th');
            const columnasTabla = Array.from(encabezados).map((th) => th.innerText);
            setColumnas(columnasTabla);
        }
    };

    return (
        <Context.Provider value={{
            obtenerColumnasTabla,
            handleColumnaChange,
            handleFileUpload,
            handleInputChange,
            filePath,
            tableHTML,
            tableHTML2,
            columnaIndex,
            columnas,
            datosColumna,
            chartImage,
            chartImage2,
            chartImage3,
            chartImage4,
            chartImage5
        }}>
            {children}
        </Context.Provider>
    )
}