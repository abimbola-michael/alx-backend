import express from "express";
import { createClient } from "redis";
import { promisify } from "util";
const app = express();
const port = 1248;
const client = createClient();

const hgetAsync = promisify(client.hget).bind(client);
const hsetAsync = promisify(client.hset).bind(client);
const listProducts = [
  {
    itemId: 1,
    itemName: "Suitcase 250",
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: "Suitcase 450",
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: "Suitcase 650",
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: "Suitcase 1050",
    price: 550,
    initialAvailableQuantity: 5,
  },
];

function getItemById(id) {
  return listProducts.find((item) => item.itemId === id);
}
async function reserveStockById(itemId, stock) {
  await hsetAsync("item:" + itemId, "stock", stock);
}
async function getCurrentReservedStockById(itemId) {
  const reservedStock = await hgetAsync("item:" + itemId, "stock");
  return parseInt(reservedStock) || 0;
}

app.get("/list_products", (req, res) => {
  res.json(
    listProducts.map((item) => {
      return {
        itemId: item.itemId,
        itemName: item.itemName,
        price: item.price,
        initialAvailableQuantity: item.initialAvailableQuantity,
      };
    })
  );
});

app.get("/list_products/:itemId", async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);
  if (!item) {
    res.json({ status: "Product not found" });
    return;
  }
  const reservedStock = await getCurrentReservedStockById(itemId);
  const availableStock = item.initialAvailableQuantity - reservedStock;
  return res.json({
    itemId: item.itemId,
    itemName: item.itemName,
    price: item.price,
    initialAvailableQuantity: item.initialAvailableQuantity,
    currentQuantity: availableStock,
  });
});

app.get("/reserve_product/:itemId", async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);
  if (!item) {
    res.json({ status: "Product not found" });
    return;
  }
  const reservedStock = await getCurrentReservedStockById(itemId);
  const availableStock = item.initialAvailableQuantity - reservedStock;
  if (availableStock <= 0) {
    res.json({ status: "Not enough stock available", itemId: item.itemId });
    return;
  }
  await reserveStockById(itemId, availableStock - 1);
  res.json({ status: "Reservation confirmed", itemId: itemId });
});

app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
