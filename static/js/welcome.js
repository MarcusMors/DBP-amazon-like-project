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

async function get_data(t_begin, t_end) {
	let request = API + "products"
	const response = await fetch(request)
}

const [begin, end] = [0, 15]
get_data(begin, end)

let watched_element = document.getElementById("login_form__email")

function set_error_message(t_error_message_element, t_error_message) {
	t_error_message_element.textContent = ""
	t_error_message_element.textContent = t_error_message
}

input_email.addEventListener("input", function () {
	const min_length = 5
	let error_message = ""
	if (this.value == "") {
		if (at_least_one_empty_field) {
			error_message = "fill email"
		} else {
			error_message = "fill email and password"
			button.disabled = t_flag_2
		}
	}
	set_error_message(error_message_element_1, error_message)
})
