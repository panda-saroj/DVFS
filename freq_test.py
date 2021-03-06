import os
import subprocess


NUM_CORE = 4

#Sets Frequency of the available cores starting from 0 untill NUM_CORE to the specified freq
def set_freq(freq, num_core):

	set_freq_part1 = 'sudo sh -c "echo '
	set_freq_part2 = ' > /sys/devices/system/cpu/cpu'
	set_freq_part3 = '/cpufreq/scaling_setspeed"'

	get_freq_part1 = 'sudo cat /sys/devices/system/cpu/cpu'
	get_freq_part2 = '/cpufreq/cpuinfo_cur_freq'

	for core in range(num_core):
		set_freq = set_freq_part1 + str(freq) + set_freq_part2 + str(core) + set_freq_part3
	
		# print(set_freq)
		os.system(set_freq)
		print("Core {} Frequency successfully set to ...".format(core))
		get_freq = get_freq_part1 + str(core) + get_freq_part2
		os.system(get_freq)
        print("\n")

# Sets core governor to userspace starting from core 0 until num_core       
def set_gov_userspace(num_core):
	set_gov_part1 = 'sudo sh -c "echo userspace > /sys/devices/system/cpu/cpu'
	set_gov_part2 = '/cpufreq/scaling_governor"'
	
	for core in range(num_core):
		set_gov = set_gov_part1 + str(core) + set_gov_part2
		os.system(set_gov)

get_freq_str = "sudo cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies"

# result = os.system(get_freq_str, shell=True)
result = subprocess.check_output(get_freq_str, shell=True)

print("cpu0 scaling_available_frequencies ...")
print(result)

freq_list = result.split()

print(freq_list)

print("\n")

# Set the govornor to userspace so that we can change the cpu frequency from user application
set_gov_userspace(NUM_CORE)
        
# Set each core to each supported frequency
for freq in freq_list:
    print("Setting CPU core frequency to : ", freq)
    set_freq(freq, NUM_CORE)
    
freq_diff = int(freq_list[1]) - int(freq_list[0])

# increment freq by 1 less than half of the freq_diff
freq_inc1 = freq_diff//2 - 1

# increment freq by 1 more than half of the freq_diff
freq_inc2 = freq_diff//2 + 1


# Set each core to increment of freq_inc1
for freq in freq_list:
    new_freq = int(freq) + freq_inc1
    print("Setting CPU core frequency to : ", new_freq)
    set_freq(new_freq, NUM_CORE)
    
# Set each core to increment of freq_inc1
for freq in freq_list:
    new_freq = int(freq) + freq_inc2
    print("Setting CPU core frequency to : ", new_freq)
    set_freq(new_freq, NUM_CORE)
