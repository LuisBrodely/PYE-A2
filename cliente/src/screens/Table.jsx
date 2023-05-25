import React, { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import { Context } from "../context/context.jsx";

export default function Home() {
	const { handleColumnaChange, handleInputChange, handleFileUpload, columnaIndex, columnas, tableHTML, tableHTML2, filePath } = useContext(Context)

	return (
		<header>

			{
				tableHTML ?
					<div className='py-5'>
						<div>
							<h1 className="px-5 text-2xl font-bold leading-tight tracking-tight text-gray-900 pb-5">Tabla de Datos</h1>
						</div>
						<div className='table px-5' dangerouslySetInnerHTML={{ __html: tableHTML }}></div>
					</div>
					:
					<div className='flex justify-center mt-5'>
						<div>
							<div className='flex justify-center'>
								<h1 className="text-2xl font-bold leading-tight tracking-tight text-gray-900">Cargar archivo</h1>

							</div>
							<input type="text"
								className='p-2.5 w-[500px] mt-3 mb-2 border border-gray-400 block'
								value={filePath}
								onChange={handleInputChange}
								placeholder="Ruta absoluta del archivo"
							/>
							<button
								onClick={handleFileUpload}
								className='w-[500px] bg-red-500 p-2.5 text-white'
							>
								Subir
							</button>
						</div>
					</div>
			}
		</header>
	)
}
