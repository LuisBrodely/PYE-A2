import React, { useContext } from 'react';
import { Context } from '../context/context';

export default function Frecuency() {
	const { chartImage, chartImage2, chartImage3, chartImage4, chartImage5, tableHTML2, tableHTML3, tableHTML4 } = useContext(Context)

	return (
		<div className='px-8 pb-10 mt-5 flex justify-center'>
			<div>
				<h1 className="text-2xl font-bold leading-tight tracking-tight text-gray-800 mb-5">Tabla de Frecuencias</h1>
				{
					tableHTML2 &&
					<>
						<div className='table mb-10' dangerouslySetInnerHTML={{ __html: tableHTML2 }}></div>
					</>

				}
				{
					tableHTML3 &&
					<>
						<div className='table mb-10' dangerouslySetInnerHTML={{ __html: tableHTML3 }}></div>
					</>

				}
				{
					tableHTML4 &&
					<>
						<div className='table mb-10' dangerouslySetInnerHTML={{ __html: tableHTML4 }}></div>
					</>

				}
			</div>
		</div>
	)
}
