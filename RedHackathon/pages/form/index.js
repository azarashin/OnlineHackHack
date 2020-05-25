import { useState } from 'react'
import {
  Button,
  Input,
  TextareaAutosize,
} from '@material-ui/core'
import { makeStyles, styled } from '@material-ui/core/styles'
import ChipInput from 'material-ui-chip-input'
import axios from 'axios'
import Image from 'material-ui-image'

const useStyles = makeStyles({
  container: {
    textAlign: "center",
  },
  url: {
    width: "70vw",
  },
  image: {
    margin: "auto",
    width: "200px",
    height: "auto",
  },
  describe: {
    width: "70vw",
    marginBottom: "5px",
  },
  inputFile: {
    width: "50vw",
    marginBottom: "5px",
  },
  inputTitle: {
    width: "60vw",
    marginBottom: "5px",
  },
  inputId: {
    width: "30vw",
    marginBottom: "5px",
  },
})

const param = {
  auth: {
    api_key: process.env.API_KEY,
    api_secret: process.env.API_SECRET,
  },
  wait: true,
}

const Form = () => {
  const [userId, setUserId] = useState('')
  const [url, setUrl] = useState('')
  const [chips, setChips] = useState([])
  const [describe, setDescribe] = useState('')
  const [roles, setRoles] = useState([])
  const [title, setTitle] = useState('')
  const classes = useStyles()

  const fillAll = () =>
    url.length !== 0 && userId.length !== 0 && chips.length !== 0 && describe.length !== 0 && roles.length !== 0 && title.length !== 0
  const clearAll = () => {
    setUserId('')
    setUrl('')
    setChips([])
    setDescribe('')
    setRoles([])
    setTitle('')
  }

  const getImageUrl = async (files) => {
    const file = files.item(0)
    const formData = new FormData()
    formData.append('data', JSON.stringify(param))
    formData.append('upload', file)
    try {
      const res = await axios.post('https://api.kraken.io/v1/upload', formData)
      setUrl(res.data.kraked_url)
    } catch (e) {
      console.error(e)
    }
  }

  const post = async () => {
    try {
      await axios.post('https://pit-creation.com/OnlineHackHack_z9eNYhrdTGvBdYsAkPrdU8Wd/post_idea',
        {
          title,
          url,
          user_id: userId,
          tags: chips,
          describe,
          roles,
        })
      clearAll()
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div className={classes.container}>
      <div>
        <div>ユーザーID</div>
        <Input value={userId} className={classes.inputId} onChange={(e) => {
          setUserId(e.target.value)
        }} />
        <div>タイトル</div>
        <Input value={title}  className={classes.inputTitle} onChange={(e) => {
          setTitle(e.target.value)
        }} />
      </div>
      <div>
        <div>アイデアスケッチ</div>
        <div className={classes.image}>
          <Image src={url} />
        </div>
        <Input type="file" className={classes.input} onChange={async e => {
          await getImageUrl(e.target.files)
        }} />
      </div>
      <div>説明</div>
      <TextareaAutosize rowsMin={4} value={describe} onChange={(e) => setDescribe(e.target.value)} className={classes.describe} />
      <div>タグを付ける</div>
      <ChipInput
        value={chips}
        onAdd={(chip) => setChips([chip, ...chips])}
        onDelete={(_, index) => setChips(chips.filter((_, i) => index !== i))}
        className={classes.inputFile}
      />
      <div>ハッカソンでの役割</div>
      <ChipInput
        value={roles}
        onAdd={(role) => setRoles([role, ...roles])}
        onDelete={(_, index) => setRoles(roles.filter((_, i) => index !== i))}
        className={classes.inputFile}
      />
      <div>
        <Button variant="contained" color="primary" disabled={!fillAll()} onClick={post}>
          投稿する
        </Button>
      </div>
    </div>
  )
}

export default Form
