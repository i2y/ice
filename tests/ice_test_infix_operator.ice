# +
func plus_case_1() {
  1 + 1
    + 1
}

func result_plus_case_1() {
  3
}

func plus_case_2() {
  1
  + 1
  + 1
}

func result_plus_case_2() {
  3
}

func plus_case_3() {
  if False {
    10 + 20 +
    30
  }
  else {
    1 + 1
      + 1
  }
}

func result_plus_case_3() {
  3
}

# -
func minus_case_1() {
  1 - 1
    - 1
}

func result_minus_case_1() {
  -1
}

func minus_case_2() {
  1
  - 1
  - 1
}

func result_minus_case_2() {
  -1
}

func minus_case_3() {
  if False {
    10 - 20 -
    30
  }
  else {
    1 - 1
      - 1
  }
}

func result_minus_case_3() {
  -1
}

# |>
func pipeline_case_1() {
  10 |> ((n) => n + 3)()
     |> ((n) => n + 4)()
     |> ((n) => n + 3)()
}

func result_pipeline_case_1() {
  20
}

func pipeline_case_2() {
  10
  |> ((n) => n + 3)()
  |> ((n) => n + 4)()
  |> ((n) => n + 3)()
}

func result_pipeline_case_2() {
  20
}

func pipeline_case_3() {
  10
  |> ((n) => n + 3)()
  |> ((n) => n + 4)()
  |> ((n) => n + 3)()
}

func result_pipeline_case_3() {
  20
}

# and
func and_case_1() {
  True and
  True
  and False
}

func result_and_case_1() {
  False
}

# or
func or_case_1() {
  False
  or False or
  True
}

func result_or_case_1() {
  True
}

# is
func is_case_1() {
  3
  is 3
}

func result_is_case_1() {
  True
}

func is_case_2() {
  3 is
  5
}

func result_is_case_2() {
  False
}

# ==
func eq_case_1() {
  3
  == 5
}

func result_eq_case_1() {
  False
}

func eq_case_2() {
  3 ==
  5
}

func result_eq_case_2() {
  False
}

# !=
func not_eq_case_1() {
  3
  != 3
}

func result_not_eq_case_1() {
  False
}

func not_eq_case_2() {
  3 !=
  3
}

func result_not_eq_case_2() {
  False
}

# gt
func gt_case_1() {
  3
  > 3
}

func result_gt_case_1() {
  False
}

func gt_case_2() {
  3 >
  1
}

func result_gt_case_2() {
  True
}

# ge
func ge_case_1() {
  3
  >= 3
}

func result_ge_case_1() {
  True
}

func ge_case_2() {
  3 >=
  1
}

func result_ge_case_2() {
  True
}

# lt
func lt_case_1() {
  3
  < 3
}

func result_lt_case_1() {
  False
}

func lt_case_2() {
  3 <
  1
}

func result_lt_case_2() {
  False
}

# le
func le_case_1() {
  3
  <= 3
}

func result_le_case_1() {
  True
}

func le_case_2() {
  3 <=
  1
}

func result_le_case_2() {
  False
}

# div
func div_case_1() {
  3
  / 3
}

func result_div_case_1() {
  1
}

func div_case_2() {
  3.0 /
  2
}

func result_div_case_2() {
  1.5
}

# times
func times_case_1() {
  3
  * 3
}

func result_times_case_1() {
  9
}

func times_case_2() {
  3.0 *
  2
}

func result_times_case_2() {
  6.0
}

# percent
func percent_case_1() {
  3
  % 3
}

func result_percent_case_1() {
  0
}

func percent_case_2() {
  3.0 %
  10
}

func result_percent_case_2() {
  3.0
}

func percent_case_3() {
  '%d'

   % 10
}

func result_percent_case_3() {
  '10'
}

# bitand
func bitand_case_1() {
  0 && 1
}

func result_bitand_case_1() {
  0
}

func bitand_case_2() {
  1
  && 0
}

func result_bitand_case_2() {
  0
}

func bitand_case_3() {
  1 &&
  1
}

func result_bitand_case_3() {
  1
}

func bitand_case_4() {
  0 && 0
}

func result_bitand_case_4() {
  0
}

# bitor
func bitor_case_1() {
  0 | 1
}

func result_bitor_case_1() {
  1
}

func bitor_case_2() {
  1 |
  0
}

func result_bitor_case_2() {
  1
}

func bitor_case_3() {
  1
  | 1
}

func result_bitor_case_3() {
  1
}

func bitor_case_4() {
  0 | 0
}

func result_bitor_case_4() {
  0
}

# bitxor
func bitxor_case_1() {
  0 ^^ 1
}

func result_bitxor_case_1() {
  1
}

func bitxor_case_2() {
  1 ^^
  0
}

func result_bitxor_case_2() {
  1
}

func bitxor_case_3() {
  1
  ^^ 1
}

func result_bitxor_case_3() {
  0
}

func bitxor_case_4() {
  0 ^^ 0
}

func result_bitxor_case_4() {
  0
}

# rshift
func rshift_case_1() {
  bin(5>>2)
}

func result_rshift_case_1() {
  '0b1'
}

func rshift_case_2() {
  bin(5
    >>3)
}

func result_rshift_case_2() {
  '0b0'
}

# lshift
func lshift_case_1() {
  bin(5<<2)
}

func result_lshift_case_1() {
  '0b10100'
}

func lshift_case_2() {
  bin(5<<
    3)
}

func result_lshift_case_2() {
  '0b101000'
}