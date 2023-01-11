import { main as generatorMain } from "zvms-apis-gen-main"

main();

function main() {
    generatorMain(process.argv.findIndex(v => v == "--noOutput") === -1);
}