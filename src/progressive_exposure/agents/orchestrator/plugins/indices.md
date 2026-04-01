# indices

Provides access to market index data (S&P 500, NASDAQ, Dow Jones) in the remote QuickJS environment.

## Import
```javascript
import * as indices from 'indices';
```

## Functions

### `indices.get()`
Returns all market indices as a JSON string.

**Returns:** string | null — JSON array of all index objects, or `null` if no data is available

### `indices.get(symbol)`
Returns a single market index by symbol as a JSON string.

**Parameters:**
- `symbol` (string) — The index symbol (e.g., `"SPX"`, `"IXIC"`, `"DJI"`)

**Returns:** string | null — JSON object for the requested index, or `null` if the symbol is not found

## Example
```javascript
import * as indices from 'indices';

// Get all indices
const allIndices = JSON.parse(indices.get());
console.log(allIndices);

// Get a single index (check for null)
const nasdaqRaw = indices.get("IXIC");
if (nasdaqRaw !== null) {
  const nasdaq = JSON.parse(nasdaqRaw);
  console.log(nasdaq.change_percent);
}
```

## Notes
- Available symbols: `SPX` (S&P 500), `IXIC` (NASDAQ), `DJI` (Dow Jones)
- Returns `null` when no results are found — always check before calling `JSON.parse()`
- When non-null, `JSON.parse()` the return value — it is a string, not an object
