import React, { useContext } from 'react';
import { Context } from '../context/context';

export default function Graphics() {
	const { chartImage, chartImage2, chartImage3, chartImage4, chartImage5, tableHTML2 } = useContext(Context)

	return (
		<>
			<div>
				<h1 className="text-3xl font-bold leading-tight tracking-tight text-gray-900">Todas las graficas</h1>
			</div>
			<div>
				{chartImage &&
					<>
						<img src={chartImage} alt="Gráfica de barras" />
						<img src={chartImage2} alt="Gráfica de pastel" />
						<img src={chartImage3} alt="Gráfica de ojivas" />
						<img src={chartImage4} alt="Gráfica de histograma" />
						<img src={chartImage5} alt="Gráfica de Poligono" />
					</>
				}
			</div>
		</>
	)
}
