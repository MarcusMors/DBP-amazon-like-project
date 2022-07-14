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

input_email.addEventListener("input", function () {
	button.disabled = this.value == ""
})
input_password.addEventListener("input", function () {
	button.disabled = this.value == ""
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
				// return Response.redirect("/") //how can i redirect or reload the page
				return
			}
			// const error_message_element = document.createElement("span")
			const error_message_element = document.getElementById("login_form__email_message")
			error_message_element.textContent = ""

			let error_message = "default data"
			if (response["id"] === +400) {
				if (response["correct_password"] == false) {
					error_message = "incorrect password"
				}
			} else if (response["id"] === +404) {
				error_message = "user not found"
			}
			error_message_element.textContent = error_message
			// error_message_element.setAttribute("class", "login_form__email_message")
			// login_form?.insertAdjacentElement("afterbegin", error_message_element)
		})
})

// getData()
