import React, { useContext } from 'react';
import { Context } from '../context/context';

export default function Graphics() {
	const { chartImage, chartImage2, chartImage3, chartImage4, chartImage5, tableHTML2 } = useContext(Context)
	console.log(chartImage)

	return ( 
		<div className='px-24'>
			<div>
				<h1 className="mt-6 text-3xl font-bold leading-tight tracking-tight text-gray-900">Todas las graficas</h1>
			</div>
			<div>
				{chartImage &&
					<div className='flex w-full justify-center'>
						<img src={chartImage} alt="Gráfica de barras" className=' w-1/2'/>
						<img src={chartImage2} alt="Gráfica de pastel" className=' w-1/2'/>
				
					</div>
				}
				{chartImage3 &&
					<div className='flex flex-wrap'>
						<img src={chartImage3} alt="Gráfica de ojivas" className='w-1/2' />
						<img src={chartImage4} alt="Gráfica de histograma" className='w-1/2'/>
						<img src={chartImage5} alt="Gráfica de Poligono" className='w-full'/>
					</div>
				}

				
			</div>
		</div>
	)
}
