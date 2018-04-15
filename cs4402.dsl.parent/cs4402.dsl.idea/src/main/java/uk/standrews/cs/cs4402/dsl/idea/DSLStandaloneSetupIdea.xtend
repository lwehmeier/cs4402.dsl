/*
 * generated by Xtext 2.10.0
 */
package uk.standrews.cs.cs4402.dsl.idea

import com.google.inject.Guice
import org.eclipse.xtext.util.Modules2
import uk.standrews.cs.cs4402.dsl.DSLRuntimeModule
import uk.standrews.cs.cs4402.dsl.DSLStandaloneSetupGenerated

class DSLStandaloneSetupIdea extends DSLStandaloneSetupGenerated {
	override createInjector() {
		val runtimeModule = new DSLRuntimeModule()
		val ideaModule = new DSLIdeaModule()
		val mergedModule = Modules2.mixin(runtimeModule, ideaModule)
		return Guice.createInjector(mergedModule)
	}
}