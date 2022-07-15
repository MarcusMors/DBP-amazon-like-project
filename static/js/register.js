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

let login_form = document.getElementById("login_form")

// let input_email = document.getElementById("login_form__email")
// let input_password = document.getElementById("login_form__password")
let button = document.getElementById("submit")

const error_message_element_general = document.getElementById("error_message_general")
const error_message_element_username = document.getElementById("error_message_username")
const error_message_element_email = document.getElementById("error_message_email")
const error_message_element_password_1 = document.getElementById("error_message_password_1")
const error_message_element_password_2 = document.getElementById("error_message_password_2")

let all_input_field = document.getElementsByClassName("log-inp")

function set_error_message(t_error_message_element, t_error_message) {
	t_error_message_element.textContent = ""
	t_error_message_element.textContent = t_error_message
}

for (let i = 0; i < 5; i++) {
	all_input_field[i].addEventListener("input", function () {
		let error_message = ""
		if (this.value == "") {
			error_message = "all fields must be filled"
			button.disabled = true
		}
		set_error_message(error_message_element_general, error_message)
	})
}

all_input_field["username"].addEventListener("input", function () {
	const min_length = 5
	let error_message = ""
	if (this.value.length <= min_length) {
		button.disabled = true
		error_message = `your username must be at least ${min_length} characters long`
	} else {
		button.disabled = false
	}
	set_error_message(error_message_element_username, error_message)
})
all_input_field["email"].addEventListener("input", function () {
	const min_length = 5
	let error_message = ""
	if (this.value.length <= min_length) {
		button.disabled = true
		error_message = `your mail must be at least ${min_length} characters long`
	} else {
		button.disabled = false
	}
	set_error_message(error_message_element_username, error_message)
})
all_input_field["password"].addEventListener("input", function () {
	const min_length = 7
	let error_message = ""
	if (this.value.length <= min_length) {
		button.disabled = true
		error_message = `your password must be at least ${min_length + 1} characters long`
	} else {
		button.disabled = false
	}
	set_error_message(error_message_element_password_1, error_message)
})
all_input_field["repeat_password"].addEventListener("input", function () {
	let error_message = ""
	if (this.value !== all_input_field["password"].value) {
		button.disabled = true
		error_message = "passwords do not match"
	} else {
		button.disabled = false
	}
	set_error_message(error_message_element_password_2, error_message)
})
// all_input_field["birthday"].addEventListener("input", function () {
// 	//
// })

login_form?.addEventListener("submit", async function (e) {
	e.preventDefault()
	const request = API + "register_user"

	const client_username = all_input_field["username"].value
	const client_email = all_input_field["email"].value
	const client_password = all_input_field["password"].value
	const client_birthday = all_input_field["birthday"].value

	const t_body = JSON.stringify({
		username: client_username,
		email: client_email,
		password: client_password,
		birthday: client_birthday,
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
			let error_message = "default data"
			if (response["id"] === +400) {
				error_message = "That user already exists or that email is already in use"
			}
			set_error_message(error_message_element_username, error_message)
		})
})

// getData()
