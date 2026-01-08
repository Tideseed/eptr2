# Unit Tests for costs.py

Comprehensive pytest test suite for all non-deprecated functions in `eptr2/util/costs.py`.

## Test Coverage

### Test Classes and Functions

1. **TestRegulationPeriod** (5 tests)
   - Tests for detecting regulation period from contract codes
   - Tests for getting starting contract codes by regulation period
   - Validates period detection (pre_2026, 26_01/current)

2. **TestKUPSTTolerance** (14 tests)
   - Tests tolerance calculations for 2026 and pre-2026 regulations
   - Tests source-specific tolerances (wind, solar, unlicensed)
   - Tests source aliasing (sun → solar)
   - Tests default tolerance values

3. **TestKUPSTCost** (16 tests)
   - Tests KUPSM (Kesinleşmiş Üretim Planından Sapma Miktarı) calculation
   - Tests unit KUPST costs for both regulations
   - Tests source-specific multipliers (battery, aggregator, unlicensed)
   - Tests with maintenance penalties
   - Tests full KUPST cost calculations with tolerance
   - Tests cost detail returns
   - Tests cost list calculations

4. **TestImbalancePrice** (10 tests)
   - Tests imbalance price calculations for 2026 and pre-2026
   - Tests price behavior when MCP > SMP, MCP < SMP, and at price limits
   - Tests custom margins and ceiling price adjustments
   - Tests price structure (positive and negative imbalances)

5. **TestImbalanceCost** (7 tests)
   - Tests imbalance cost calculations for both regulations
   - Tests costs with included prices
   - Tests cost structure validation

6. **TestCombinedPriceAndCost** (5 tests)
   - Tests combined imbalance prices and costs
   - Tests KUPST inclusion in combined calculations
   - Tests both 2026 and pre-2026 regulations

7. **TestImbalanceAmount** (10 tests)
   - Tests imbalance amount calculations for producers and consumers
   - Tests DSG (Dengeden Sorumlu Grup) tolerance calculations
   - Tests with custom tolerance multipliers
   - Tests raw vs effective imbalance calculations
   - Tests regulation-specific DSG tolerances (5% current, 10% pre-2026)

8. **TestDifferenceCosts** (5 tests)
   - Tests comprehensive cost calculations combining imbalance and KUPST
   - Tests producer vs consumer calculations
   - Tests with included quantities
   - Tests regulation period variations

9. **TestEdgeCases** (8 tests)
   - Tests with zero prices
   - Tests with very high prices
   - Tests with large forecast-actual differences
   - Tests float vs int consistency
   - Tests invalid parameter handling

10. **TestIntegration** (3 tests)
    - Full calculation chains for producers and consumers
    - Contract code-based calculations
    - Pre-2026 and current regulation workflows

## Total Test Count: 86 tests

All tests pass successfully.

## Running the Tests

```bash
# Run all tests in the file
pytest tests/test_costs.py -v

# Run specific test class
pytest tests/test_costs.py::TestKUPSTCost -v

# Run specific test
pytest tests/test_costs.py::TestKUPSTCost::test_calculate_kupsm_within_tolerance -v

# Run with coverage
pytest tests/test_costs.py --cov=eptr2.util.costs
```

## Key Functions Tested

### Regulation Management
- `get_regulation_period_by_contract()`
- `get_starting_contract_by_regulation_period()`

### KUPST Functions
- `get_kupst_tolerance()`
- `get_kupst_tolerance_by_contract()`
- `get_kupst_tolerance_pre_2026()`
- `get_kupst_tolerance_2026()`
- `calculate_unit_kupst_cost()`
- `calculate_unit_kupst_cost_by_contract()`
- `calculate_unit_kupst_cost_2026()`
- `calculate_unit_kupst_cost_pre_2026()`
- `calculate_kupsm()`
- `calculate_kupst_cost()`
- `calculate_kupst_cost_by_contract()`
- `calculate_kupst_cost_list()`

### Imbalance Price Functions
- `calculate_unit_imbalance_price()`
- `calculate_unit_imbalance_price_by_contract()`
- `calculate_unit_imbalance_price_2026()`
- `calculate_unit_imbalance_price_pre_2026()`

### Imbalance Cost Functions
- `calculate_unit_imbalance_cost()`
- `calculate_unit_imbalance_cost_by_contract()`
- `calculate_unit_imbalance_cost_2026()`
- `calculate_unit_imbalance_cost_pre_2026()`

### Combined Calculation Functions
- `calculate_unit_price_and_costs()`
- `calculate_unit_price_and_costs_by_contract()`
- `calculate_imbalance_amount()`
- `calculate_diff_costs()`

## Test Features

- **Comprehensive Coverage**: Tests all non-deprecated functions
- **Multiple Regulations**: Tests for both pre-2026 and 2026 regulations
- **Edge Cases**: Zero prices, very high prices, boundary conditions
- **Integration Tests**: Full calculation chains combining multiple functions
- **Contract-Based Tests**: Tests using contract codes for automatic regulation detection
- **Parameter Validation**: Tests for proper error handling of invalid inputs
- **Consistency Tests**: Validates float vs int price handling
- **Real-World Scenarios**: Tests producer/consumer scenarios with KUPST and imbalance calculations
