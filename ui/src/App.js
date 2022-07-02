import './App.css';
import 'antd/dist/antd.css';
import {Button, Table} from "antd";
import Header from "./Header/Header";

const dataSource = [
  {
    key: '1',
    name: 'Mike',
    age: 32,
    address: '10 Downing Street',
  },
  {
    key: '2',
    name: 'John',
    age: 42,
    address: '10 Downing Street',
  },
];

const columns = [
  {
    title: 'Объявление',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: 'Age',
    dataIndex: 'age',
    key: 'age',
    defaultSortOrder: 'descend',
    sorter: () => null,
  },
  {
    title: 'Address',
    dataIndex: 'address',
    key: 'address',
    defaultSortOrder: 'descend',
    sorter: () => null,
  },
];

function App() {
  const onChange = (pagination, filters, sorter, extra) => {
    console.log('params', pagination, filters, sorter, extra);
  };
  return (
    <div className="App">
      <Header/>
      <div className="grabber-content">
        <div className="grabber-content__header">Последнее обновление: 4 часа назад<Button type="primary">Обновить</Button></div>
        <Table dataSource={dataSource} columns={columns} onChange={onChange}/>;
      </div>
    </div>
  );
}

export default App;
