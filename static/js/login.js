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
// async function getData() {
// 	let request = API + "check_credentials"
// 	const response = await fetch(API)
// }

let login_form = document.getElementById("login_form")

let input_email = document.getElementById("login_form__email")
let input_password = document.getElementById("login_form__password")
let button = document.getElementById("submit")

const error_message_element_1 = document.getElementById("error_message_1")
const error_message_element_2 = document.getElementById("error_message_2")

let at_least_one_empty_field = false

function set_error_message(t_error_message_element, t_error_message) {
	t_error_message_element.textContent = ""
	t_error_message_element.textContent = t_error_message
}
function set_flag_and_button_disabled(t_flag_1, t_flag_2) {
	at_least_one_empty_field = t_flag_1
	button.disabled = t_flag_2
}

input_email.addEventListener("input", function () {
	const min_length = 5
	let error_message = ""
	if (this.value == "") {
		if (at_least_one_empty_field) {
			error_message = "fill email"
		} else {
			error_message = "fill email and password"
			set_error_message(error_message_element_2, "")
		}
		set_flag_and_button_disabled(true, true)
	} else if (this.value.length <= min_length) {
		set_flag_and_button_disabled(false, true)
		error_message = `your email must be at least ${min_length} characters long`
	} else {
		set_flag_and_button_disabled(false, false)
	}
	set_error_message(error_message_element_1, error_message)
})
input_password.addEventListener("input", function () {
	const min_length = 7
	let error_message = ""
	if (this.value == "") {
		error_message = "fill password"
		set_flag_and_button_disabled(true, true)
	} else if (this.value.length <= min_length) {
		set_flag_and_button_disabled(false, true)
		error_message = `your password must be at least ${min_length + 1} characters long`
	} else {
		set_flag_and_button_disabled(false, false)
	}
	set_error_message(error_message_element_2, error_message)
})

login_form?.addEventListener("submit", async function (e) {
	e.preventDefault()
	const request = API + "check_credentials"

	const client_email = input_email.value
	const client_password = input_password.value

	const t_body = JSON.stringify({
		email: client_email,
		password: client_password,
	})

	console.log(t_body)

	fetch(request, {
		method: "POST",
		body: t_body,
		headers: {
			"content-type": "application/json; charset=UTF-8",
		},
	})
		.then(function (response) {
			return response.json()
		})
		.then(function (data) {
			console.log(data)
			return data
		})
		.then(function (response) {
			if (response["id"] === +200) {
				window.location.reload()
				return
			}
			error_message_element_1.textContent = ""

			let error_message = ""
			if (response["id"] === +400) {
				if (response["correct_password"] == false) {
					error_message = "incorrect password"
				}
			} else if (response["id"] === +404) {
				error_message = "user not found"
			}
			set_error_message(error_message_element_1, error_message)
		})
})

// getData()
