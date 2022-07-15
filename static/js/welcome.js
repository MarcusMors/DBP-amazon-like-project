// Copyright (C) 2022 José Enrique Vilca Campana
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as
// published by the Free Software Foundation, either version 3 of the
// License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

const API = "http://localhost:5000/api/"

let insert_guide_element = document.getElementById("insert_guide")

/**
 * @param {number} t_begin
 * @param {number} t_end
 */
function get_data(t_begin, t_end) {
	let request = API + "products"
	fetch(request, {
		method: "POST",
		body: JSON.stringify({
			begin: t_begin,
			end: t_end,
		}),
		headers: { "content-type": "application/json; charset=UTF-8" },
	})
		.then(function (response) {
			return response.json()
		})
		.then(function (response) {
			console.log(response)
			let products = response["products"]

			for (let i = 0; i < products.length; i++) {
				const filename = products[i]["filename"]

				let anchor_container = document.createElement("a")
				let div_container = document.createElement("div")
				anchor_container.append(div_container)
				anchor_container.setAttribute("class", "product-ref")
				anchor_container.setAttribute("href", filename)
				div_container.setAttribute("class", "product-container")

				let product_title = document.createElement("p")
				let product_description = document.createElement("p")
				let product_price = document.createElement("p")
				let product_image = document.createElement("img")
				div_container.append(
					product_price,
					product_description,
					product_title,
					product_image
				)

				product_title.append(products[i]["title"])
				product_description.append(products[i]["description"])
				product_price.append(products[i]["price"])

				product_image.setAttribute("src", "images/" + filename)

				insert_guide_element?.appendChild(anchor_container)
			}
		})
}

const [begin, end] = [0, 9]
get_data(begin, end)

let signal_element = document.getElementById("load_signal")
// let load_button = document.getElementById("load")

/**
 * @param {{ textContent: string; }} t_error_message_element
 * @param {string} t_error_message
 */
function set_error_message(t_error_message_element, t_error_message) {
	t_error_message_element.textContent = ""
	t_error_message_element.textContent = t_error_message
}
