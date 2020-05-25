import { useState, useEffect } from 'react'
import {
  Card,
  CardHeader,
  CardContent,
  Typography,
  TextareaAutosize,
  Button,
} from '@material-ui/core'
import { makeStyles } from '@material-ui/core/styles'
import axios from 'axios'

const useStyles = makeStyles({
  container: {
    textAlign: "center",
    display: "flex",
    flexDirection: "row",
    overflowX: "scroll",
  },
  card: {
    minWidth: 400,
    maxWidth: 450,
    margin: "0 5px"
  },
  img: {
    width: "400px",
  },
  comment: {
    width: "350px",
  },
})

const List = () => {
  const classes = useStyles()
  const [data, setData] = useState([])
  const [uuid, setUuid] = useState('')
  const [comment, setComment] = useState('')
  useEffect(() => {
    let unmounted = false
    const f = async () => {
      const res = await axios.get('https://pit-creation.com/OnlineHackHack_z9eNYhrdTGvBdYsAkPrdU8Wd/idea_list')
      const data = await res.data
      if (!unmounted) {
        setData(data)
      }
    }
    f()
    const cleanup = () => {
      unmounted = true
    }
    return cleanup
  }, [])

  const post = async () => {
    try {
      await axios.post('', { comment, uuid })
      setComment('')
      setUuid('')
    } catch (e) {
      console.log(e)
    }
  }

  return (
    <div className={classes.container}>
      {data.map(d =>
        <Card className={classes.card}>
          <CardHeader
            title={`${d.user_id}「${d.title}」`}
          />
          <img className={classes.img} src={d.idea_url.split('?').length === 1 ? d.idea_url : d.idea_url.split('?')[0]} />
          <CardContent>
            <Typography paragraph>{`投票数：${d.count ?? 0}`}</Typography>
          </CardContent>
          <CardContent>
            <Typography paragraph>説明:</Typography>
            <Typography paragraph>
              {d.describe_data}
            </Typography>
          </CardContent>
          <CardContent>
            <Typography paragraph>タグ:</Typography>
            {d.tag.split(',').length === 1 ?
              <Card>
                {d.tag}
              </Card> :
              d.tag.split(',').map(t =>
                <Card>
                  {t}
                </Card>
              )
            }
          </CardContent>
          <CardContent>
            <Typography paragraph>コメントする:</Typography>
            <TextareaAutosize rowsMin={4} value={comment} onChange={
              (e) => {
                setComment(e.target.value)
                setUuid(d.uuid)
              }} className={classes.comment} />
            <br />
            <Button variant="contained" color="primary" disabled={comment.length === 0} onClick={post}>
              送信
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default List
