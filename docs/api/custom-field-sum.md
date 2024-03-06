# Custom field sum

Following scripts output the sum of all values stored in a custom field for documents matching certain criteria.

## Sum of single field

```python title="custom-field-sum.py"
--8<-- "scripts/api/custom-field-sum/custom-field-sum.py"
```


## Sum of difference of two fields

Appears to be an exotic use-case. But imagine having two custom fields for an invoice: gross and net value.
To get to know the sum of all taxes paid, you will need to sum up the differences of both custom fields. As simple as that :)

```python title="custom-field-sum-of-differences.py"
--8<-- "scripts/api/custom-field-sum/custom-field-sum-of-differences.py"
```
