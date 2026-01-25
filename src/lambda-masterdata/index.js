import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, ScanCommand } from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const dynamodb = DynamoDBDocumentClient.from(client);

export const handler = async (event) => {
  const tableName = process.env.MASTER_TABLE_NAME;
  const path = event.path || event.rawPath || "";

  try {
    if (path === "/master/ingredients") {
      const result = await dynamodb.send(
        new ScanCommand({
          TableName: tableName,
          FilterExpression: "begins_with(PK, :pk)",
          ExpressionAttributeValues: {
            ":pk": "ING#"
          }
        })
      );

      const ingredients = (result.Items || []).map((item) => ({
        ingredientId: item.ingredientId,
        ingredientName: item.ingredientName,
        category: item.category,
        allergens: item.allergens || [],
        defaultUnit: item.defaultUnit,
        status: item.status
      }));

      return {
        statusCode: 200,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({ ingredients })
      };
    }

    return {
      statusCode: 404,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({ message: "Not found" })
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
