import express from "express"
const router = express.Router()
import dupCompareController from "../controllers/dup-compare"

router.post("/compare",
    // middlewares
    dupCompareController.getCompareResults
)

export default router