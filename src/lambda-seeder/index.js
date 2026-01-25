import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, PutCommand } from "@aws-sdk/lib-dynamodb";

const client = new DynamoDBClient({});
const dynamodb = DynamoDBDocumentClient.from(client);

const INGREDIENTS = [
  { ingredientId: "ING-001", ingredientName: "Cocoa Liquor", category: "COCOA", allergens: [], defaultUnit: "%", status: "ACTIVE" },
  { ingredientId: "ING-002", ingredientName: "Cocoa Butter", category: "FAT", allergens: [], defaultUnit: "%", status: "ACTIVE" },
  { ingredientId: "ING-003", ingredientName: "Sugar", category: "SWEETENER", allergens: [], defaultUnit: "%", status: "ACTIVE" },
  { ingredientId: "ING-004", ingredientName: "Milk Powder", category: "DAIRY", allergens: ["MILK"], defaultUnit: "%", status: "ACTIVE" },
  { ingredientId: "ING-005", ingredientName: "Milk Fat", category: "DAIRY_FAT", allergens: ["MILK"], defaultUnit: "%", status: "ACTIVE" },
  { ingredientId: "ING-006", ingredientName: "Soy Lecithin", category: "EMULSIFIER", allergens: ["SOY"], defaultUnit: "%", status: "ACTIVE" },
  { ingredientId: "ING-007", ingredientName: "Sunflower Lecithin", category: "EMULSIFIER", allergens: [], defaultUnit: "%", status: "ACTIVE" },
  { ingredientId: "ING-008", ingredientName: "PGPR", category: "EMULSIFIER", allergens: [], defaultUnit: "%", status: "ACTIVE" },
  { ingredientId: "ING-009", ingredientName: "Vanilla Flavor", category: "FLAVOR", allergens: [], defaultUnit: "ppm", status: "ACTIVE" },
  { ingredientId: "ING-010", ingredientName: "Salt", category: "MINOR_INGREDIENT", allergens: [], defaultUnit: "ppm", status: "ACTIVE" },
  { ingredientId: "ING-011", ingredientName: "Almond Pieces", category: "INCLUSION", allergens: ["TREE_NUTS"], defaultUnit: "%", status: "ACTIVE" },
  { ingredientId: "ING-012", ingredientName: "Crisped Rice", category: "INCLUSION", allergens: [], defaultUnit: "%", status: "ACTIVE" }
];

export const handler = async () => {
  const tableName = process.env.MASTER_TABLE_NAME;

  try {
    for (const ingredient of INGREDIENTS) {
      await dynamodb.send(
        new PutCommand({
          TableName: tableName,
          Item: {
            PK: `ING#${ingredient.ingredientId}`,
            SK: "META",
            ...ingredient
          }
        })
      );
    }

    return {
      statusCode: 200,
      body: JSON.stringify({ message: "Ingredient seeding completed" })
    };
  } catch {
    return {
      statusCode: 500,
      body: JSON.stringify({ message: "Seeding failed" })
    };
  }
};
