import { useState, useEffect } from "react"
import "./dup-compare.css"
import DupCompareService from "./dup-compare.service"
import { ToastService } from "../../shared/toast.service"
import { Severity } from "../../shared/constants"
import { useLocation } from "react-router-dom"
import * as _ from 'lodash'

const Mode = {
  Text: 'text',
  Url: 'url'
}

const DupCompare = (props) => {
  const routeInfo = useLocation()
  const passedState = routeInfo.state
  const { urlA, urlB } = passedState
  const defaultModeA = urlA ? Mode.Url : Mode.Text
  const defaultModeB = urlB ? Mode.Url : Mode.Text
  const [sourceMode, setSourceMode] = useState(defaultModeA)
  const [targetMode, setTargetMode] = useState(defaultModeB)
  const [sourceText, setSourceText] = useState('')
  const [targetText, setTargetText] = useState('')
  const [sourceUrl, setSourceUrl] = useState(urlA)
  const [targetUrl, setTargetUrl] = useState(urlB)
  const [sourceSegements, setSourceSegments] = useState([])
  const [targetSegements, setTargetSegments] = useState([])
  const [resultPairs, setResultPairs] = useState([])
  const [compareResult, setCompareResult] = useState({})
  const [loading, setLoading] = useState(false)

  const toastService = new ToastService()
  const simCheckService = new DupCompareService()

  useEffect(() => {
    if (urlA && urlB) {
      checkSimilarity()
    }
  }, [])

  const checkSimilarity = () => {
    // TODO: handle url vs url and url vs text
    const sourceContent = sourceMode === Mode.Text ? sourceText : sourceUrl
    const targetContent = targetMode === Mode.Text ? targetText : targetUrl
    const compareOption = { sourceMode, sourceContent, targetMode, targetContent }
    setLoading(true)
    simCheckService.getSimilarityResults(compareOption)
      .then(response => {
        const responseData = response.data || {}
        const compareResult = responseData.results || {}
        setCompareResult(compareResult)
      })
      .catch((error) => {
        toastService.displayToast(error.response, Severity.Error)
        setCompareResult({})
      })
      .finally(_ => setLoading(false))
  }

  useEffect(() => {
    console.log('compareResult: ', compareResult)
    const sourceSegements = compareResult.segmentListA || []
    const targetSegements = compareResult.segmentListB || []
    const resultPairs = compareResult.pairs || []
    const sortedResultPairs = _.orderBy(resultPairs, ['similarityScore'], ['desc'])
    setSourceSegments(sourceSegements)
    setTargetSegments(targetSegements)
    setResultPairs(sortedResultPairs)
  }, [compareResult])

  const getBtnClass = (sourceMode, btnLabel) => {
    return sourceMode === btnLabel
      ? "layout-cell btn btn-primary btn-sm"
      : "layout-cell btn btn-outline-secondary btn-sm"
  }

  const urlInput = (underlyingValue, setUnderlyingValue) => (
    <form className="full-width margin-horizontal--xs">
      <div className="input-group mb-3">
        <input type="text" className="form-control bg--white" placeholder="URL"
          aria-label="Username" aria-describedby="basic-addon1"
          value={underlyingValue} onChange={($event) => setUnderlyingValue($event.target.value)} />
      </div>
    </form>
  )

  const textInput = (underlyingValue, setUnderlyingValue) => (
    <form className="full-width margin-horizontal--xs">
      <div className="input-group mb-3">
        <textarea type="text" className="form-control bg--white" placeholder="Nội dung"
          aria-label="Username" aria-describedby="basic-addon1" rows={10}
          value={underlyingValue} onChange={($event) => setUnderlyingValue($event.target.value)}>
        </textarea>
      </div>
    </form>
  )

  const sourceContentRenderer = () => {
    return sourceMode === Mode.Text
      ? textInput(sourceText, setSourceText)
      : urlInput(sourceUrl, setSourceUrl)
  }

  const targetContentRenderer = () => {
    return targetMode === Mode.Text
      ? textInput(targetText, setTargetText)
      : urlInput(targetUrl, setTargetUrl)
  }

  const resultRenderer = (segments, segmentIdx) => {
    const prevIdx = segmentIdx - 1
    const nextIdx = segmentIdx + 1
    const prevParam = segments[prevIdx] ? <span>{segments[prevIdx]}</span> : ''
    const nextParam = segments[nextIdx] ? <span>{segments[nextIdx]}</span> : ''
    const currParam = <span style={{ color: 'orange' }}>{segments[segmentIdx]}</span>
    return (
      <>{prevParam} {currParam} {nextParam}</>
    )
  }

  const resultPairsRenderer = () => {
    return resultPairs.map(pair => {
      const sourceSegIdx = pair.segmentIdxA
      const targetSegIdx = pair.segmentIdxB
      return (
        <>
          <div class="row margin-bottom--xs">
            <div className="col layout-cell"> {resultRenderer(sourceSegements, sourceSegIdx)} </div>
            <div className="col layout-cell"> {resultRenderer(targetSegements, targetSegIdx)} </div>
          </div>
          <hr />
        </>
      )
    })
  }

  return (
    <div className="dup-compare-container">
      <div className="layout-grid margin-bottom--20">
        <div className="layout-cell flex-fill dup-compare-title">Nhập liên kết hoặc nội dung cần so sánh</div>
      </div>
      <div className="row">
        <div className="col layout-cell">
          <div className="layout-grid">
            <button type="button" className={getBtnClass(sourceMode, Mode.Text)} onClick={() => setSourceMode(Mode.Text)}>Text</button>
            <button type="button" className={getBtnClass(sourceMode, Mode.Url)} onClick={() => setSourceMode(Mode.Url)}>URL</button>
          </div>
          <div className="layout-grid">
            {sourceContentRenderer()}
          </div>
        </div>
        <div className="col layout-cell">
          <div className="layout-grid">
            <button type="button" className={getBtnClass(targetMode, Mode.Text)} onClick={() => setTargetMode(Mode.Text)}>Text</button>
            <button type="button" className={getBtnClass(targetMode, Mode.Url)} onClick={() => setTargetMode(Mode.Url)}>URL</button>
          </div>
          <div className="layout-grid">
            {targetContentRenderer()}
          </div>
        </div>
      </div>
      <div className="layout-grid margin-bottom--20" style={{ 'justify-content': 'flex-end' }}>
        <button type="button" className="btn btn-warning compare-btn" onClick={checkSimilarity}>So sánh</button>
      </div>
      <div class="full-width margin-bottom--xs">
        <h4>Kết quả: </h4>
        <span>Số cặp trùng {resultPairs.length}</span>
      </div>
      {loading ? <div className="sr-list-container centered-container"> <h2>Loading...</h2> </div> : resultPairsRenderer()}
    </div >

  )
}

export default DupCompare

