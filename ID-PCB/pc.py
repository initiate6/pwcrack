from async_subprocess import AsyncPopen, PIPE
import time

def main():
    args = ("hashcat-cli32.exe", "-m 100", "-a 3", "-n 2", "A0.M100.hash", "?a?a?a?a?a")
    process = AsyncPopen(args,
                            stdin=PIPE,
                            stdout=PIPE,
                            stderr=PIPE
                            )
    retcode = process.poll()
    while retcode == None:
        stdoutdata, stderrdata = process.communicate('\n')
        if stderrdata:
            print stderrdata
        if stdoutdata:
            print stdoutdata
        time.sleep(5)
        retcode = process.poll()


main()
