# stocks

Provides access to stock quote data in the remote QuickJS environment.

## Import
```javascript
import * as stocks from 'stocks';
```

## Functions

### `stocks.get()`
Returns all stock quotes as a JSON string.

**Returns:** string | null — JSON array of all stock quote objects, or `null` if no data is available

### `stocks.get(ticker)`
Returns a single stock quote by ticker as a JSON string.

**Parameters:**
- `ticker` (string) — The stock ticker (e.g., `"AAPL"`, `"MSFT"`, `"NVDA"`)

**Returns:** string | null — JSON object for the requested stock, or `null` if the ticker is not found

## Example
```javascript
import * as stocks from 'stocks';

// Get all stocks
const allStocks = JSON.parse(stocks.get());
console.log(allStocks);

// Get a single stock (check for null)
const appleRaw = stocks.get("AAPL");
if (appleRaw !== null) {
  const apple = JSON.parse(appleRaw);
  console.log(apple.price);
}
```

## Notes
- Returns `null` when no results are found — always check before calling `JSON.parse()`
- When non-null, `JSON.parse()` the return value — it is a string, not an object
