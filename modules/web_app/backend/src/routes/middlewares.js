import Joi from "joi"
import jwt from "jsonwebtoken"
import { secretKey } from "../configs"
import { CODE } from "../constants"
import { schema } from "../validations/schema"

export const isVerifiedToken = async (req, res, next) => {
  if (req.get("Authorization") === undefined) {
    res.json({
      code: CODE.INVALID_TOKEN,
      message: "Thiếu dữ liệu Authorization và Access Token"
    })
    return
  }
  const accessToken = req.get("Authorization")
  if (accessToken) {
    jwt.verify(accessToken, secretKey, async (err, decoded) => {
      if (err) {
        res.json({
          code: CODE.INVALID_TOKEN,
          message: "Không thể xác thực token",
          error: err
        })
      } else {
        next()
      }
    })

  } else {
    res.json({
      code: CODE.INVALID_TOKEN,
      message: "Access token không được để rỗng!"
    })
  }
}

const fieldValidation = (input, template) => {
  for (let item of template) {
    if (!Object.prototype.hasOwnProperty.call(input, item)) {
      return item
    }
  }
  return null
}

// check data field when request
export const requiredField = async (req, response, body, params, query, next) => {
  const bodyChecked = fieldValidation(req.body, body)
  const queryChecked = fieldValidation(req.query, query)
  const paramChecked = fieldValidation(req.params, params)

  if (bodyChecked) {
    response
      .status(CODE.MISSING_BODY)
      .json({ message: `Missing! You are missing body field: [${bodyChecked}]` })
    return
  }

  if (queryChecked) {
    response
      .status(CODE.MISSING_QUERY)
      .json({ message: `Missing! You are missing body field: [${queryChecked}]` })
    return
  }

  if (paramChecked) {
    response
      .status(CODE.MISSING_QUERY)
      .json({ message: `Missing! You are missing body field: [${paramChecked}]` })
    return
  }

  next()
}

export const validateField = async (req, response, next) => {
  const bodyChecked = Joi.validate(req.body, schema)
  const queryChecked = Joi.validate(req.query, schema)
  const paramChecked = Joi.validate(req.params, schema)
  if (bodyChecked.error) {
    response
      .status(CODE.INVALID_PARAMS)
      .json({ message: `Lỗi định dạng dữ liệu - ${bodyChecked.error.details}` })
    return
  }

  if (queryChecked.error) {
    response
      .status(CODE.INVALID_QUERY)
      .json({ message: `Lỗi định dạng dữ liệu - ${queryChecked.error.details}` })
    return
  }

  if (paramChecked.error) {
    response
      .status(CODE.MISSING_BODY)
      .json({ message: `Lỗi định dạng dữ liệu - ${paramChecked.error.details}` })
    return
  }

  next()
}


