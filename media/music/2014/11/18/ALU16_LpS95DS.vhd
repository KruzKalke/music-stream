----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    21:10:43 09/21/2014 
-- Design Name: 
-- Module Name:    ALU16 - Data Flow 
-- Project Name: 
-- Target Devices: 
-- Tool versions: 
-- Description: 
--
-- Dependencies: 
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: 
--
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.std_logic_unsigned.all;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity ALU16 is

generic (data_width : INTEGER := 16;
			sel_width : INTEGER := 2);

port (a_in : in std_logic_vector(data_width-1 downto 0);
		b_in : in std_logic_vector(data_width-1 downto 0);
		sel : in std_logic_vector(sel_width-1 downto 0);
		result : out std_logic_vector(data_width-1 downto 0);
		cout : out std_logic;
		lt, eq, gt : out std_logic;
		overflow : out std_logic	);
end entity ALU16;

------ selection operations ------
----------------------------------
-- sel	operation
-- 00		add
-- 01		subtract
-- 10		and
-- 11		or
----------------------------------

------- conditional operations ---
-- lt = 1 for a<b
-- eq = 1 for a=b
-- gt = 1 for a>b
-- cout = carry out from arithmetic operations
-- overflow = 2's complement addition 
-----------------------------------

architecture dataflow of ALU16 is

--temporyary signals
signal temp : std_logic_vector(data_width downto 0) := b"00000000000000000";
signal zero : std_logic_vector(data_width downto 0) := b"00000000000000000";

begin

with sel select
		temp <=	a_in + b_in + zero when "00",
					a_in - b_in + zero when "01",
					a_in and b_in + zero when "10",
					a_in or b_in + zero when "11";
					
result <= temp(data_width-1 downto 0);
cout <= temp(data_width);

lt <= '1' when a_in < b_in else
		'0';
eq <= '1' when a_in = b_in else
		'0';
gt <= '1' when a_in > b_in else 
		'0';		

with sel select
		overflow <=	(a_in(data_width-1) and b_in(data_width-1) and not(temp(data_width-1))) or (not(a_in(data_width-1)) and not(b_in(data_width-1)) and temp(data_width-1)) when "00",
						(a_in(data_width-1) and not(b_in(data_width-1)) and not(temp(data_width-1))) or (not(a_in(data_width-1)) and b_in(data_width-1) and temp(data_width-1)) when "01",
						'0' when "10",
						'0' when "11";

end dataflow;

