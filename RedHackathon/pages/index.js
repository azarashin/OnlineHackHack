import {
  ListItem,
  ListItemText
} from '@material-ui/core'
import { makeStyles } from '@material-ui/core/styles'

const useStyles = makeStyles({
  container: {
    textAlign: "center",
  },
})

const ListItemLink = (props) => <ListItem button component="a" {...props} />;


const Home = () => {
  const classes = useStyles()

  return (
    <div className={classes.container}>
      <ListItemLink href="/form">
        <ListItemText primary="アイデアを投稿する" />
      </ListItemLink>
      <ListItemLink href="/list">
        <ListItemText primary="他の人のアイデアを見る" />
      </ListItemLink>
    </div>
  )
}

export default Home
