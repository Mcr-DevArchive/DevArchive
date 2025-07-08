.PHONY: format

format:
	@echo "🔍 Running sed to rename Spanish variables/functions to English..."
	sed -i 's/tamanio_m2/size_m2/g' scraper/*.py
	sed -i 's/habitaciones/rooms/g' scraper/*.py
	sed -i 's/localidad/location/g' scraper/*.py
	sed -i 's/descripcion/description/g' scraper/*.py
	sed -i 's/datos/data/g' scraper/*.py
	sed -i 's/todas_propiedades/all_properties/g' scraper/*.py
	sed -i 's/url_por_pagina/url_for_page/g' scraper/*.py
	sed -i 's/guardar_csv/save_to_csv/g' scraper/*.py
	sed -i 's/enviar_telegram/send_csv_to_telegram/g' scraper/*.py

	@echo "🎨 Running black to autoformat..."
	black .

	@echo "📚 Running isort to sort imports..."
	isort .

	@echo "✅ Done! All code renamed and formatted."

