import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, PutCommand } from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const dynamodb = DynamoDBDocumentClient.from(client);

export const handler = async (event) => {
  const tableName = process.env.TABLE_NAME;

  try {
    const body = JSON.parse(event.body || "{}");

    const item = {
      id: `${Date.now()}`,
      productId: body.productId || "UNKNOWN",
      data: body.data || "",
      timestamp: body.timestamp || new Date().toISOString()
    };

    await dynamodb.send(
      new PutCommand({
        TableName: tableName,
        Item: item
      })
    );

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({ message: "Success", id: item.id })
    };
  } catch {
    return {
      statusCode: 500,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({ message: "Internal server error" })
    };
  }
};
