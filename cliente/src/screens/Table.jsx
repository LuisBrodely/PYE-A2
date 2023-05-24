import React, { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import { Context } from "../context/context.jsx";

export default function Home() {
	const { handleColumnaChange, handleInputChange, handleFileUpload, columnaIndex, columnas, tableHTML, tableHTML2, filePath } = useContext(Context)

	return (
		<>
			<header>
				<div>
					<h1 className="text-3xl font-bold leading-tight tracking-tight text-gray-900">Subir archivo</h1>
				</div>

				{
					tableHTML ?
						<>
							<label htmlFor="columna">Seleccionar columna:</label>
							<select id="columna" value={columnaIndex} onChange={handleColumnaChange}>
								{columnas.map((columna, index) => (
									<option value={columna} key={index}>
										{columna}
									</option>
								))}
							</select>
							<div className='table' dangerouslySetInnerHTML={{ __html: tableHTML }}></div>
						</>
						:
						<>
							<input type="text" value={filePath} onChange={handleInputChange} placeholder="Ruta absoluta del archivo" />
							<button onClick={handleFileUpload}>Enviar</button>
						</>
				}
			</header>
		</>
	)
}
