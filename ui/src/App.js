import './App.css';
import 'antd/dist/antd.css';
import {Button, Table} from "antd";
import Header from "./Header/Header";
import {useEffect, useState} from "react";
import axios from "axios";

const columns = [
  {
    title: 'Объявление',
    dataIndex: 'name',
    key: 'name',
    sorter: () => null,
  },
  {
    title: 'Цена',
    dataIndex: 'price',
    key: 'price',
    sorter: () => null,
  },
  {
    title: 'Оценка',
    dataIndex: 'rating',
    key: 'rating',
    sorter: () => null,
  },
  {
    title: 'Описание',
    dataIndex: 'description',
    key: 'description',
  },
  {
    title: 'Дата',
    dataIndex: 'updated_at',
    key: 'updated_at',
    sorter: () => null,
  },
  {
    title: 'Действия',
    dataIndex: 'url',
    key: 'url',
  },
];

function App() {

  const onChange = (pagination, filters, sorter, extra) => {
    let order = ""
    if (sorter.order === "ascend") order = `&ordering=-${sorter.field}`
    if (sorter.order === "descend") order = `&ordering=${sorter.field}`
    setOrderBy(order)
    setPagination({...pagination, current: pagination.current})
  };
  const [pagination, setPagination] = useState({
    current: 1,
  });
  const [data, setData] = useState([])
  const [orderBy, setOrderBy] = useState("&ordering=-rating")

  useEffect(() => {
    axios.get(`/api/ads/?page=${pagination.current}${orderBy}`)
      .then((response) => {
        setData(response.data.results.map(data => ({
            "key": data.id,
            "name": data.name,
            "price": <p style={{whiteSpace: "nowrap"}}>{data.price}</p>,
            "rating": data.rating,
            "description": <p className="table-description">{data.description}</p>,
            "updated_at": new Date(data.updated_at).toLocaleString("RU-ru"),
            "url": <a
              href={data.url} target="_blank">open</a>
          }))
        )
        if (!pagination.total) setPagination({...pagination, total: response.data.count})
      })
  }, [orderBy, pagination])


  return (
    <div className="App">
      <Header/>
      <div className="grabber-content">
        <div className="grabber-content__header">Последнее обновление: 4 часа назад<Button
          type="primary">Обновить</Button></div>
        <Table
          className="grabber-content__table"
          dataSource={data}
          columns={columns}
          onChange={onChange}
          pagination={pagination}
        />;
      </div>
    </div>
  );
}

export default App;
