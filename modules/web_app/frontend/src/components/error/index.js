import React from "react"
import { Nav } from "react-bootstrap"

function ErrorPage() {
  return (
    <div class="page-wrap d-flex flex-row align-items-center">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-12 text-center">
            <span class="display-1 d-block">404</span>
            <div class="mb-4 lead">Trang web không tồn tại.</div>
            <Nav.Link href="/">Về trang chính</Nav.Link>
          </div>
        </div>
      </div>
    </div>
  )
}
export default ErrorPage